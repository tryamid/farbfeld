"""
Implementation of the [Suckless' Farbfeld][1] image format.

Farbfeld is a lossless image format without any compression,
stores raw RGB pixels.
Each sub-pixel is 16-bit and each pixel has four-components
`Red`,`Green`,`Blue`,`Alpha` which makes each pixel size 64-bit.

[1]: https://tools.suckless.org/farbfeld/
"""

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

__all__ = ['FarbfeldEncodeError', 'FarbfeldDecodeError',
           'FarbfeldEncoder', 'FarbfeldDecoder']

from decode import *
from encode import *