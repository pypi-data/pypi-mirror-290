from pathlib import Path
from typing import NamedTuple, Optional

import jax
import jax.numpy as jnp
import numpy as np

from pantea.logger import logger
from pantea.types import Array, Dtype, default_dtype


def _to_jax_int(n: int) -> Array:
    return jnp.array(n, dtype=default_dtype.INT)


class DescriptorScalerStats(NamedTuple):
    """Scaler statistical quantities."""

    nsamples: Array = _to_jax_int(0)
    mean: Array = jnp.array([])
    sigma: Array = jnp.array([])
    minval: Array = jnp.array([])
    maxval: Array = jnp.array([])


class DescriptorScalerParams(NamedTuple):
    """Scaler parameters."""

    scale_min: Array
    scale_max: Array


@jax.jit
def _init_scaler_stats_from(data: Array) -> DescriptorScalerStats:
    return DescriptorScalerStats(
        nsamples=_to_jax_int(data.shape[0]),
        mean=jnp.mean(data, axis=0),
        sigma=jnp.std(data, axis=0),
        maxval=jnp.max(data, axis=0),
        minval=jnp.min(data, axis=0),
    )


@jax.jit
def _fit_scaler(stats: DescriptorScalerStats, data: Array) -> DescriptorScalerStats:
    # Calculate stats for a new batch of data
    new_mean: Array = jnp.mean(data, axis=0)
    new_sigma: Array = jnp.std(data, axis=0)
    new_min: Array = jnp.min(data, axis=0)
    new_max: Array = jnp.max(data, axis=0)
    m, n = stats.nsamples, data.shape[0]
    # Calculate scaler new stats for the entire data
    mean = m / (m + n) * stats.mean + n / (m + n) * new_mean
    sigma = jnp.sqrt(
        m / (m + n) * stats.sigma**2
        + n / (m + n) * new_sigma**2
        + m * n / (m + n) ** 2 * (stats.mean - new_mean) ** 2
    )
    maxval = jnp.maximum(stats.maxval, new_max)
    minval = jnp.minimum(stats.minval, new_min)
    nsamples = stats.nsamples + n
    return DescriptorScalerStats(nsamples, mean, sigma, minval, maxval)


@jax.jit
def _center(stats: DescriptorScalerStats, array: Array) -> Array:
    return array - stats.mean


@jax.jit
def _scale(
    params: DescriptorScalerParams, stats: DescriptorScalerStats, array: Array
) -> Array:
    return params.scale_min + (params.scale_max - params.scale_min) * (
        array - stats.minval
    ) / (stats.maxval - stats.minval)


@jax.jit
def _scale_center(
    params: DescriptorScalerParams, stats: DescriptorScalerStats, array: Array
) -> Array:
    return params.scale_min + (params.scale_max - params.scale_min) * (
        array - stats.mean
    ) / (stats.maxval - stats.minval)


@jax.jit
def _scale_center_sigma(
    params: DescriptorScalerParams, stats: DescriptorScalerStats, array: Array
) -> Array:
    return (
        params.scale_min
        + (params.scale_max - params.scale_min) * (array - stats.mean) / stats.sigma
    )


@jax.jit
def _get_number_of_warnings(stats: DescriptorScalerStats, array: Array) -> Array:
    if array.ndim == 2:
        gt = jax.lax.gt(array, stats.maxval[None, :])
        lt = jax.lax.gt(stats.minval[None, :], array)
    else:
        gt = jax.lax.gt(array, stats.maxval)
        lt = jax.lax.gt(stats.minval, array)
    return jnp.any(jnp.logical_or(gt, lt))  # alternative counting is using sum


class DescriptorScaler:
    """
    Scale descriptor values.

    Scaling parameters are calculated by fitting over the samples in the dataset.
    Available scaler information are as follows:

    * mean
    * sigma (standard deviation)
    * maxval
    * minval

    This descriptor scaler is also used to warn when setting out-of-distribution samples base
    on the fitted scaler parameters.
    """

    def __init__(
        self,
        scale_type: str = "scale_center",
        scale_min: float = 0.0,
        scale_max: float = 1.0,
    ) -> None:
        """Initialize scaler including scaler type and min/max values."""
        assert scale_min < scale_max

        # Set min/max range for scaler
        self.scale_type = scale_type
        self.params = DescriptorScalerParams(
            scale_min=jnp.array(scale_min),
            scale_max=jnp.array(scale_max),
        )

        # Statistical parameters
        self.dimension: int = 0
        self.stats = DescriptorScalerStats()

        self.number_of_warnings: int = 0
        self.max_number_of_warnings: Optional[int] = None

        # Set scaler type function
        self._transform = getattr(self, f"{self.scale_type}")

    def fit(self, data: Array) -> None:
        """
        Fit descriptor scaler internal stats using the input data.
        Bach-wise sampling is also possible (see `this`_ for more details).

        .. _this: https://notmatthancock.github.io/2017/03/23/simple-batch-stat-updates.html
        """
        data = jnp.atleast_2d(data)  # type: ignore

        if self.stats.nsamples == 0:
            self.dimension = data.shape[1]
            self.stats = _init_scaler_stats_from(data)
        else:
            if data.shape[1] != self.dimension:
                logger.error(
                    f"Data dimension doesn't match: {data.shape[1]} (expected {self.dimension})",
                    exception=ValueError,
                )
            self.stats = _fit_scaler(self.stats, data)

    def __call__(self, array: Array, warnings: bool = False) -> Array:
        """
        Transform the input descriptor values based on the scaler parameters.

        This method has to be called after fitting scaler over the dataset,
        or statistical parameters are already loaded (e.g. saved file).
        """
        if warnings:
            self._check_warnings(array)
        return self._transform(array)

    def set_max_number_of_warnings(self, number: Optional[int] = None) -> None:
        """Set the maximum number of warning for out of range descriptor values."""
        self.max_number_of_warnings = number
        self.number_of_warnings = 0
        logger.debug(
            f"Setting the maximum number of scaler warnings: {self.max_number_of_warnings}"
        )

    def _check_warnings(self, array: Array) -> None:
        """
        Check whether the output scaler values exceed the predefined min/max range values or not.

        If it's the case, it keeps counting the number of warnings and
        raises an error when it exceeds the maximum number.

        An out of range descriptor value is in fact an indication of
        the descriptor extrapolation which has to be avoided.
        """
        if self.max_number_of_warnings is None:
            return

        self.number_of_warnings += int(_get_number_of_warnings(self.stats, array))

        if self.number_of_warnings >= self.max_number_of_warnings:
            logger.warning(
                "Exceeding maximum number scaler warnings (extrapolation warning): "
                f"{self.number_of_warnings} (max={self.max_number_of_warnings})"
            )

    def center(self, array: Array) -> Array:
        return _center(self.stats, array)

    def scale(self, array: Array) -> Array:
        return _scale(self.params, self.stats, array)

    def scale_center(self, array: Array) -> Array:
        return _scale_center(self.params, self.stats, array)

    def scale_center_sigma(self, array: Array) -> Array:
        return _scale_center_sigma(self.params, self.stats, array)

    def save(self, filename: Path) -> None:
        """Save scaler parameters into file."""
        logger.debug(f"Saving scaler parameters into '{str(filename)}'")
        with open(str(filename), "w") as file:
            file.write(f"{'# Min':<23s} {'Max':<23s} {'Mean':<23s} {'Sigma':<23s}\n")
            for i in range(self.dimension):
                file.write(
                    f"{self.stats.minval[i]:<23.15E}"
                    f"{self.stats.maxval[i]:<23.15E}"
                    f"{self.stats.mean[i]:<23.15E}"
                    f"{self.stats.sigma[i]:<23.15E}\n"
                )

    def load(self, filename: Path, dtype: Optional[Dtype] = None) -> None:
        """Load scaler parameters from file."""
        logger.debug(f"Loading scaler parameters from '{str(filename)}'")
        data = np.loadtxt(str(filename)).T
        dtype = dtype if dtype is not None else default_dtype.FLOATX
        self.dimension = data.shape[1]
        self.stats = DescriptorScalerStats(
            nsamples=_to_jax_int(1),
            mean=jnp.array(data[2], dtype=dtype),
            sigma=jnp.array(data[3], dtype=dtype),
            minval=jnp.array(data[0], dtype=dtype),
            maxval=jnp.array(data[1], dtype=dtype),
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(scale_type='{self.scale_type}', "
            f"scale_min={self.params.scale_min}, scale_max={self.params.scale_max})"
        )

    def __bool__(self) -> bool:
        return False if len(self.stats.mean) == 0 else True
