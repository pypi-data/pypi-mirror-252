#!/usr/bin/env python3
"""eminus - A plane wave density functional theory code.

Minimal usage example to do a DFT calculation for helium::

   from eminus import Atoms, SCF
   atoms = Atoms('He', (0, 0, 0))
   SCF(atoms).run()
"""
from . import config
from .atoms import Atoms
from .cell import Cell
from .dft import get_epsilon, get_psi
from .io import (
    read,
    read_cube,
    read_json,
    read_traj,
    read_xyz,
    write,
    write_cube,
    write_json,
    write_pdb,
    write_traj,
    write_xyz,
)
from .logger import log
from .scf import RSCF, SCF, USCF
from .version import __version__, info

__all__ = ['config', 'Atoms', 'Cell', 'get_epsilon', 'get_psi', 'info', 'log', 'read', 'read_cube',
           'read_json', 'read_traj', 'read_xyz', 'RSCF', 'SCF', 'USCF', 'write', 'write_cube',
           'write_json', 'write_pdb', 'write_traj', 'write_xyz', '__version__']


def demo():
    """Fast demo calculation for helium."""
    atoms = Atoms('He', (0, 0, 0), ecut=5)
    SCF(atoms).run()
