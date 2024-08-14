
.. .. image:: docs/images/logo.png
..         :alt: logo
        
======
Pantea
======


.. image:: https://img.shields.io/pypi/v/pantea.svg
        :target: https://pypi.python.org/pypi/pantea

.. image:: https://github.com/hghcomphys/pantea/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/hghcomphys/pantea/blob/main/.github/workflows/tests.yml

.. image:: https://readthedocs.org/projects/pantea/badge/?version=latest
        :target: https://pantea.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


Description
-----------
Pantea is an optimized Python library on basis of Google `JAX`_ that enables 
development of machine learning inter-atomic potentials 
for use in computational physics. 
These potentials are necessary for conducting large-scale molecular 
dynamics simulations of complex materials with ab initio accuracy.

.. _JAX: https://github.com/google/jax


See `documentation`_ for more information.

.. _documentation: https://pantea.readthedocs.io/en/latest/readme.html


Features
--------
* The design of Pantea is `simple` and `flexible`, which makes it easy to incorporate atomic descriptors and potentials. 
* It uses `automatic differentiation` to make defining new descriptors straightforward.
* Pantea is written purely in Python and optimized with `just-in-time` (JIT) compilation.
* It also supports `GPU-accelerated` computing, which can significantly speed up preprocessing and model training.

.. warning::
        This package is under heavy development and the current focus is on the implementation of high-dimensional 
        neural network potential (HDNNP) proposed by Behler et al. 
        (`2007 <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.98.146401>`_).


Installation
------------
To install Pantea, run this command in your terminal:

.. code-block:: console

    $ pip install pantea

For machines with an NVIDIA **GPU** please follow the
`installation <https://pantea.readthedocs.io/en/latest/installation.html>`_ 
instruction on the documentation. 


Examples
--------

---------------------------
Defining an ACSF descriptor
---------------------------
This script demonstrates the process of evaluating an array of atomic-centered symmetry functions (`ACSF`_) 
for a specific element, which can be utilized to evaluate the descriptor values for any structure. 
The resulting values can then be used to construct a machine learning potential.

.. _ACSF: https://aip.scitation.org/doi/10.1063/1.3553717


.. code-block:: python

        from pantea.datasets import Dataset
        from pantea.descriptors import ACSF
        from pantea.descriptors.acsf import CutoffFunction, G2, G3

        # Read atomic structure dataset (e.g. water molecules)
        structures = Dataset.from_runner('input.data')
        structure = structures[0]
        print(structure)
        # >> Structure(natoms=12, elements=('H', 'O'), dtype=float64)

        # Define an ACSF descriptor for hydrogen
        # It includes two radial (G2) and angular (G3) symmetry functions
        descriptor = ACSF('H')
        cfn = CutoffFunction.from_cutoff_type(r_cutoff=12.0, cutoff_type='tanh')
        descriptor.add(G2(cfn, eta=0.5, r_shift=0.0), 'H')
        descriptor.add(G3(cfn, eta=0.001, zeta=2.0, lambda0=1.0, r_shift=12.0), 'H', 'O')
        print(descriptor)
        # >> ACSF(central_element='H', symmetry_functions=2)

        values = descriptor(structure)
        print("Descriptor values:\n", values)
        # >> Descriptor values:
        # [[0.01952943 1.13103234]
        #  [0.01952756 1.04312263]
        # ...
        #  [0.00228752 0.41445455]]

        gradient = descriptor.grad(structure, atom_index=0)
        print("Descriptor gradient:\n", gradient)
        # >> Descriptor gradient:
        # [[ 0.04645236 -0.05037861 -0.06146214]
        # [-0.10481855 -0.01841708  0.04760214]]


-------------------------
Training an NNP potential
-------------------------
This example illustrates how to quickly create a `high-dimensional neural network 
potential` (`HDNNP`_) instance from an in input setting files and train it on input structures. 
The trained potential can then be used to evaluate the energy and force components for new structures.

.. _HDNNP: https://pubs.acs.org/doi/10.1021/acs.chemrev.0c00868


.. code-block:: python

        from pantea.datasets import Dataset
        from pantea.potentials import NeuralNetworkPotential

        structures = Dataset.from_runner("input.data")
        structure = structures[0]

        nnp = NeuralNetworkPotential.from_file("input.nn")

        nnp.fit_scaler(structures)
        nnp.fit_model(structures)

        total_energy = nnp(structure)
        print(total_energy)

        forces = nnp.compute_forces(structure)
        print(forces)


Example files: `input.data`_ and `input.nn`_

.. _input.data: https://drive.google.com/file/d/1VMckgIv_OUvCOXQ0pYzaF5yl9AwR0rBy/view?usp=sharing
.. _input.nn: https://drive.google.com/file/d/15Oq9gAJ2xXVMcHyWXlRukfJFevyVO7lI/view?usp=sharing



License
-------
This project is licensed under the GNU General Public License (GPL) version 3 - 
see the `LICENSE <https://github.com/hghcomphys/pantea/blob/main/LICENSE>`_ file for details.
