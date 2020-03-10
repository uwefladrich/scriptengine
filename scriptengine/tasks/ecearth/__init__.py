""" ScriptEngine EC-Earth tasks

This module provides SE tasks for the EC-Earth ESM
"""

from .eceinfo import UpdateEceinfo, WriteEceinfo
from .slurm import Sbatch


def taskmap():
    return {'update_eceinfo': UpdateEceinfo,
            'write_eceinfo': WriteEceinfo,
            'sbatch': Sbatch}
