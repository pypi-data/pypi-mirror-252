from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            name='retinawhitenoise._rng',
            sources=['rng/rng.pyx'],
            depends=['rng/rng_gasdev_ran1.cpp', 'rng/rng_gasdev_ran1.h'],
            include_dirs=['rng'],
            language="c++",
        ),
    ]
)
