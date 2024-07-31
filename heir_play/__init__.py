"""A magic for running heir-opt nightly binary"""
__version__ = '0.0.1'

from .heir_opt import load_nightly
from .heir_opt import HeirOptMagic

def load_ipython_extension(ipython):
    ipython.register_magics(HeirOptMagic)
