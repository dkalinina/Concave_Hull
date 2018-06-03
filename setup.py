from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os

setup(
  name = 'cython alpha shapes',
  ext_modules = cythonize(["cython_alpha_shapes.pyx"])
)