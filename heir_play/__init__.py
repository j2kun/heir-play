"""A magic for running heir-opt nightly binary"""
__version__ = '0.0.1'

from .heir_opt import load_nightly
from .heir_opt import HeirOptMagic

def load_ipython_extension(ipython):
    binary_path = load_nightly()
    magic = HeirOptMagic(ipython, binary_path=str(binary_path))
    ipython.register_magics(magic)
