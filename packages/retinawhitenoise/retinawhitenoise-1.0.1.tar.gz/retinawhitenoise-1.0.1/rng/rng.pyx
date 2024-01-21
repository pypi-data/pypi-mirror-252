# distutils: language=c++
# cython: language_level=3
"""
Scalar and vector implementation of the gasdev and ran1 pseudo-random
number generators from Numerical Recipes (with an additional boolean
version ranb)

Example
-------
>>> from whitenoise import Rng
>>> r = Rng(-1000)
>>> r.ran1(3)
[0.19059444460579866, 0.4645137076566525, 0.928777586169903]
>>> r.ranb(3)
[1, 0, 1]
>>> r.gasdev(3)
[1.1028967066460202, 1.073456607462508, 1.0344341091633127]

Notes
-----
Based on ran1 and gasdev from Numerical Recipes, ported to Cython from
the ran1 and gasdev mex files by Christian Mendl, see
https://github.com/gollischlab/RecreateWhiteNoiseStimuliWithMatlab

Seed can be either a negative integer or a seed dictionary.

For Windows and Python 2.7, you might need to install Visual Studio 2008
(or the Visual Studio C++ Tools for Python 2.7).
(Fernando Rozenblit, 2017)

Modified to add ranb and improve performance.
(Sören Zapp, 2018)

Fixed compile flags for newer setuptools.
(Sören Zapp, 2021)

Changed to OOP, added documentation (doc strings), revised installation,
changed to Python 3.
(Sören Zapp, 2023)
"""

cdef extern from "rng_gasdev_ran1.h":
    struct Seed:
        long idum
        long iy
        long iv[32]  # const long NTAB = 32
        int iset
        double gset

cdef extern from "rng_gasdev_ran1.cpp":
    list c_ran1_vec "ran1_vec" (Seed& seed, unsigned int num)
    list c_ranb_vec "ranb_vec" (Seed& seed, unsigned int num)
    double c_gasdev "gasdev" (Seed& seed)

cdef class Rng:
    """Pseudo-random number generator"""
    cdef Seed c_seed

    def __init__(self, seed):
        """
        Pseudo-random number generator

        Parameters
        ----------
        seed : int or dict
            Seed can be either a negative integer or a Seed dictionary
        """
        self.seed = seed

    @property
    def seed(self):
        """Current seed"""
        return self.c_seed

    @seed.setter
    def seed(self, seed):
        self._make_seed(seed)

    cpdef _make_seed(self, seed):
        if isinstance(seed, dict):
            self.c_seed = seed
        else:
            self.c_seed.idum = seed

    cpdef ran1(self, n=1):
        """
        Generate sequence of pseudo-random values in [0,1)

        Parameters
        ----------
        n : int, optional
            Number of values to sample. Default is 1

        Returns
        -------
        ret : float or list of float
            Generated values
        """
        return c_ran1_vec(self.c_seed, n)

    cpdef ranb(self, n=1):
        """
        Generate binary sequence of pseudo-random numbers

        Parameters
        ----------
        n : int, optional
            Number of values to sample. Default is 1

        Returns
        -------
        ret : int or list of int
            Generated values (0 or 1)
        """
        return c_ranb_vec(self.c_seed, n)

    cpdef gasdev(self, n=1):
        """
        Generate sequence of pseudo-random standard Gaussian deviates

        Parameters
        ----------
        n : int, optional
            Number of values to sample. Default is 1

        Returns
        -------
        ret : float or list of float
            Generated values
        """
        return ([c_gasdev(self.c_seed) for x in range(n)] if n > 1
                else c_gasdev(self.c_seed))
