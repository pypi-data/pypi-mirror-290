from functools import partial
from typing import Dict, Protocol

import jax.numpy as jnp
from frozendict import frozendict
from jax import jit

from pantea.atoms.structure import Inputs
from pantea.descriptors import DescriptorScaler
from pantea.descriptors.acsf.acsf import _calculate_descriptor
from pantea.descriptors.descriptor import DescriptorInterface
from pantea.models import NeuralNetworkModel
from pantea.types import Array, Element


class AtomicPotentialInterface(Protocol):
    """An interface for AtomicPotential."""

    descriptor: DescriptorInterface
    scaler: DescriptorScaler
    model: NeuralNetworkModel


@partial(jit, static_argnums=(0,))
def _compute_atomic_energy(
    atomic_potential: AtomicPotentialInterface,
    positions: Array,
    params: frozendict,
    inputs: Inputs,
) -> Array:
    """Compute model output per-atom energy."""
    x = _calculate_descriptor(
        atomic_potential.descriptor,
        positions,
        inputs.positions,
        inputs.atom_types,
        inputs.lattice,
        inputs.emap,
    )
    x = atomic_potential.scaler(x)
    atomic_energy = atomic_potential.model.apply({"params": params}, x)
    return atomic_energy  # type: ignore


@partial(jit, static_argnums=(0,))
def _energy_fn(
    atomic_potential: Dict[Element, AtomicPotentialInterface],
    positions: Dict[Element, Array],
    params: Dict[Element, frozendict],
    inputs: Dict[Element, Inputs],
) -> Array:
    """
    A helper function that allows to calculate gradient of the NNP total energy
    respect to the atom positions (for each element).
    """
    elements: list[Element] = list(inputs.keys())
    total_energy: Array = jnp.array(0.0)
    for element in elements:
        atomic_energy = _compute_atomic_energy(
            atomic_potential[element],
            positions[element],
            params[element],
            inputs[element],
        )
        total_energy += jnp.sum(atomic_energy)
    return total_energy


_compute_energy = _energy_fn
