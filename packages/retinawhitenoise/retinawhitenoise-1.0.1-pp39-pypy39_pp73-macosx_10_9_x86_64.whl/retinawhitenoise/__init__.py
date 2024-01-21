"""
Routines to recreate binary and Gaussian white noise stimuli
"""
__version__ = '1.0.1'
__all__ = [
    'Rng',
    'binarystimulus',
    'gaussianstimulus',
]

try:
    from ._rng import Rng
except ModuleNotFoundError:
    class NotInstalledError(Exception):
        pass
    raise NotInstalledError(
        'Please follow the installation instructions'
    ) from None

from . import binarystimulus
from . import gaussianstimulus
