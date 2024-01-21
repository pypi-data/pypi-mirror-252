# RecreateWhiteNoiseStimuliWithPython

[![Build status](https://github.com/gollischlab/RecreateWhiteNoiseStimuliWithPython/actions/workflows/pypi.yml/badge.svg)](https://github.com/gollischlab/RecreateWhiteNoiseStimuliWithPython/deployments/PyPI)
[![PyPI version](https://img.shields.io/pypi/v/retinawhitenoise.svg)](https://pypi.python.org/pypi/retinawhitenoise)

Code for regenerating the random-number-based contrast values applied in experiments with white-noise stimulation in the Gollisch Lab.
Used for both temporal and spatiotemporal stimuli, and for both binary and Gaussian white noise.

The random-number sequences are needed for analyzing the spike responses of recorded cells under white-noise stimulation.

### Installation
A full installation of the package is done from command-line using `pip` with
```
pip install retinawhitenoise
```

#### Manual installation
If the `pip` package is not available for a given operating system or Python version, the package and Cython code can be compiled manually instead.
```
pip install https://github.com/gollischlab/RecreateWhiteNoiseStimuliWithPython/archive/main.tar.gz
```

Windows might require the [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools) to be installed (including *"Windows SDK"* and *"MSVC ... C++ x64/x86 build tools"*). For details, see [here](https://www.scivision.dev/python-windows-visual-c-14-required).

### Usage
The Python package `retinawhitenoise` offers two modules `binarystimulus` and `gaussianstimulus`,
each offering routines to `recreate`, `save` (to disk), and `load` stimulus sequences.

Instructions on how to use them with example code and explanations is included in the jupyter notebook `examples.ipynb`.
