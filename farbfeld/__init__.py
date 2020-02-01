"""
Implementation of the [Suckless' Farbfeld][1] image format.

Farbfeld is a lossless image format which store 16-bit raw
pixels in the RGBA pixelformat.

[1]: https://tools.suckless.org/farbfeld/
"""

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

__all__ = ['FarbfeldEncodeError', 'FarbfeldDecodeError',
           'FarbfeldEncoder', 'FarbfeldDecoder']

from .decode import *
from .encode import *