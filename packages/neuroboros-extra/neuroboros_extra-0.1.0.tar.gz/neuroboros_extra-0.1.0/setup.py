import numpy
from Cython.Build import cythonize
from setuptools import setup

setup(
    name="neuroboros-extra",
    ext_modules=cythonize("src/nb_extra/*/*.pyx"),
    include_dirs=[numpy.get_include()],
)
