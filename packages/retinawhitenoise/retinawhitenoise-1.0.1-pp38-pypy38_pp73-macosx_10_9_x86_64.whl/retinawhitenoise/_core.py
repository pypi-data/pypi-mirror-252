"""
Internal super functions

The keyword argument `mode` may be either 1 for binary white noise or
0 for Gaussian white noise.
"""
import h5py
import numpy as np
from pathlib import Path
import re
from tqdm import tqdm, trange

from . import Rng

__all__ = []  # Not meant for user imports


# Adjustable
PRECISION = 'float32'  # Or 'float64' for Gaussian white noise
COMPRESSION = 3  # H5 compression for writing stimulus to disk

# Internal
_pattern = re.compile(r'\d{4}\.h5$')  # File matching


def recreate(seed, xy=(), num_frames=1, num_trials=1, progress=False, mode=1):
    """
    Recreate temporal or spatiotemporal white noise stimulus for a given
    set of parameters trial-by-trial to iterate over on the fly

    Parameters
    ----------
    seed : int or dict
        Initial seed

    xy : tuple, optional
        Dimensions of the spatial frame, e.g. `(x, y)` for two spatial
        dimensions, `(s,)` for one spatial dimension, or `()` for no
        spatial component, that is, only temporal white noise, i.e. full
        field flicker. Default is `()`

    num_frames : int, optional
        Number of spatial frames. Default is 1

    num_trials : int, optional
        Number of trials. This determines the number of values to yield.
        Default is 1

    progress : dict or bool, optional
        Arguments to pass to tqdm progress bar. If True, a tqdm progress
        bar is shown with its default properties. If False, no progress
        bar is shown. If dict, it serves as keyword arguments passed to
        tqdm. Default is False

    Yields
    ------
    stim : (*xy, num_frames) numpy.ndarray
        Recreated stimulus per trial of type np.int8 containing -1 and 1

    Notes
    -----
    The function does not return the stimulus. Instead it yields it for
    each trial iteratively. Alternatively, the stimulus can first be
    recreated and saved to disk to later load specific sections of it on
    demand using `save` and `load`.

    Example
    -------
    Recreating the stimulus on the fly (as opposed to first saving and
    loading it from disk on demand) for 20 frames of 200 x 150 spatial
    size, iterating over 5 trials can be achieved like so

    >>> for stim in recreate(-1000, (200, 150), 20, 5):
    >>>   pass  # At each iteration stim is a (200, 150, 20) array

    Enable tqdm progress bar and specify arguments

    >>> for stim in recreate(-1000,
    >>>                      xy=(200, 150),
    >>>                      num_frames=20,
    >>>                      num_trials=5,
    >>>                      progress=dict(desc='Running', leave=True)):
    >>>   pass  # The progress bar remains visible with a custom title

    """
    if progress and num_trials > 1:
        kwargs = dict(desc='Recreating stimulus', unit='trial', leave=False)
        if isinstance(progress, dict):
            kwargs.update(progress)
        itr = trange(num_trials, **kwargs)
    else:
        itr = range(num_trials)

    shape = (*xy, num_frames)
    size = np.prod(shape)
    stim = np.empty(shape, dtype='int8' if mode else PRECISION)
    stimf = np.moveaxis(stim, -1, 0)

    r = Rng(seed)

    # Duplicated, with if-block outside to avoid 'if' at every iteration
    if mode:
        for _ in itr:
            stimf.flat = r.ranb(size)
            stim[stim == 0] = -1
            yield stim
    else:
        for _ in itr:
            stimf.flat = r.gasdev(size)
            yield stim


def save(basepath, seed, *args, mode=1, **kwargs):
    """
    Recreate temporal or spatiotemporal white noise stimulus for a given
    set of parameters and write it to disk

    Parameters
    ----------
    basepath : str or pathlib.Path
        File path including base file name to store the stimulus

    seed : int or dict
        Initial seed

    Other Parameters
    ----------------
    See recreate. Tqdm progress bar is here enabled by default.

    See also
    --------
    recreate : Recreate white noise stimulus
    """
    basepath = Path(basepath).expanduser().resolve()
    if basepath.is_dir():
        basepath = basepath / 'stim'
    if basepath.suffix == '.h5':
        basepath = basepath.parent / basepath.stem
    if basepath.name[-1] in '0123456789':
        basepath = basepath.parent / (basepath.name + '_')
    basepath.parent.mkdir(exist_ok=True, parents=True)

    # Enable progress bar if not explicitly disabled
    tqdm_args = dict(desc='Saving stimulus', leave=True)
    if len(args) < 4:  # 4th argument is progress
        arg_3 = kwargs.get('progress', True)
        kwargs['progress'] = tqdm_args if arg_3 is not False else arg_3
    else:
        args = list(args)
        arg_3 = args[3]
        args[3] = tqdm_args if arg_3 is not False else arg_3
    if isinstance(arg_3, dict):
        tqdm_args.update(arg_3)

    # Call recreate and store results
    for i, stim in enumerate(recreate(seed, *args, **kwargs, mode=mode)):
        with h5py.File(str(basepath) + f'{i:04.0f}.h5', mode='w') as f:
            f.create_dataset('stim', data=stim, compression=COMPRESSION)


def load(basepath, crop=slice(None), num=None, progress=False):
    """
    Load previously saved temporal or spatiotemporal white noise
    stimulus from disk to iterate over trial-by-trial (loading only a
    specific spatial window and section of trials)

    Parameters
    ----------
    basepath : str or pathlib.Path
        File path including base file name to read the stimulus from.
        The base file name as created by `save` consists of an arbitrary
        prefix. The function then considers all matching file names
        followed by a four digit trial number and a .h5 file extension

    crop : slice or tuple of slice, optional
        Slice(s) of the stimulus frame. This is useful to only load a
        specific spatial region of the stimulus at the benefit of lower
        loading time and memory consumption. Default is slice(None)

    num : int, range, tuple, or array_like, optional
        Specify files/trials to iterate over. The trial number
        corresponds to the four digit file name suffix as created by
        `save`. If int, specify the number of trials starting from zero.
        If range, specify range of trials. If array_like, specify exact
        trial indices. If None, all trials are considered. Default is
        None

    progress : dict or bool, optional
        Arguments to pass to tqdm progress bar. If True, a tqdm progress
        bar is shown with its default properties. If False, no progress
        bar is shown. If dict, it serves as keyword arguments passed to
        tqdm. Default is False

    Yields
    ------
    stim : (x, y, num_frames) numpy.ndarray
        Recreated stimulus per trail, possibly spatially sliced (see
        `crop`)

    Raises
    ------
    ValueError :
        If `basepath` does not include a base file name

    ValueError :
        If `num` is provided in invalid format

    Notes
    -----
    The files to load are expected in the format as created by `save`:
    "basename0004.h5" with an arbitrary prefix followed by a four digit
    trial number. If there is only one or no trials, the base name is
    followed by '0000'. To load only one specific file (trial), still
    provide the base name common to all trials and specify the trial
    number through `num`, see Examples.

    Examples
    --------
    Load only trials 2 to 5 in the previously saved stimulus with a
    specific spatial window

    >>> basename = '/path/to/basename'  # No trial number and extension
    >>> trials = range(2, 5)  # Iterate over trials 2, 3, and 4
    >>> window = (slice(23, 45), slice(12, 51))  # Rectangle of x and y
    >>>
    >>> for stim in load(basename, crop=window, num=trials)
    >>>   pass  # At each iteration stim is a (22, 39, frames) array

    Load only one specific trial (one file)

    >>> load(basename, num=4)  # Loads basename0004.h5
    """
    basepath = Path(basepath).expanduser().resolve()
    if basepath.is_dir():
        raise ValueError('Base file name missing. File name is directory.')
    if basepath.suffix == '.h5':
        basepath = basepath.parent / basepath.stem
    basepath = basepath.parent / basepath.name.rstrip('0123456789')

    # Build sorted list of valid files
    filelist = sorted(basepath.parent.glob(basepath.stem + '????.h5'))
    filelist = list(map(str, filelist))  # Turn Path objects into str
    filelist = list(filter(_pattern.search, filelist))  # Validate files

    # Limited range or list of files
    if num is not None:
        if not isinstance(num, (range, list, np.ndarray)):
            num = range(num)
        if not isinstance(num, range):
            num = np.asarray(num)
            if num.dtype != np.integer or num.ndim != 1:
                raise ValueError('Indices have wrong format')
        filelist = list(x for x in filelist if int(Path(x).stem[-4:]) in num)

    # Construct progress bar
    if progress and len(filelist) > 1:
        kwargs = dict(desc='Loading stimulus', unit='trial', leave=False)
        if isinstance(progress, dict):
            kwargs.update(progress)
        itr = tqdm(filelist, **kwargs)
    else:
        itr = filelist

    # Load and yield one file (trial) at a time
    for fpath in itr:
        with h5py.File(fpath, mode='r') as f:
            yield f['stim'][crop]
