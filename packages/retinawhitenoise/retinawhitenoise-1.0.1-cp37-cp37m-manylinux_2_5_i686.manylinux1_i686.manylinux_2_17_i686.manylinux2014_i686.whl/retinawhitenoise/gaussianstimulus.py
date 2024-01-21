"""
Recreate temporal or spatiotemporal Gaussian white noise stimulus
sequence given a seed, length, and spatial dimensions if applicable

This modules offers to recreate a stimulus iteratively trial-by-trial on
the fly. Alternatively, the stimulus can first be recreated and saved to
disk to be later loaded at specific sections on demand. This is a matter
of preference (memory vs. time) and whether the stimulus is needed
several times over the course of the analysis.
"""
from . import _core

__all__ = [
    'recreate',
    'save',
    'load',
]


def recreate(seed, xy=(), num_frames=1, num_trials=1, progress=False):
    yield from _core.recreate(seed, xy, num_frames, num_trials, progress, 0)


def save(basepath, seed, *args, **kwargs):
    _core.save(basepath, seed, *args, **kwargs, mode=0)


recreate.__doc__ = _core.recreate.__doc__
save.__doc__ = _core.save.__doc__
from ._core import load  # noqa: E402
