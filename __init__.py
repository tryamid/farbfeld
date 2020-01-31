"""
Implementation of the [Suckless' Farbfeld][1] image format.

Farbfeld is a lossless image format without any compression,
stores raw RGB pixels.
Each sub-pixel is 16-bit and each pixel has four-components
`Red`,`Green`,`Blue`,`Alpha` which makes each pixel size 64-bit.

[1]: https://tools.suckless.org/farbfeld/
"""
from types import SimpleNamespace
from struct import pack, unpack
from array import array
from itertools import chain

class FarbfeldEncodeError(Exception):
    pass

class FarbfeldDecodeError(Exception):
    pass

class FarbfeldEncoder:
    "Encoder to encode 16-bit pixels into the Farbfeld image format."

    def __init__(self, width, height):
        self.width = abs(width)
        self.height = abs(height)

    def encode(self, outfile, imageframe):
        """
        outfile
            a file-like object that supports write() calls and
            support bytes as the first argument.

        imageframe
            an 2D iterable object representing an image frame
            (row-major), pixels are RGBA, bitdepth is 16-bit.
        """
        if not hasattr(outfile, 'write'):
            raise FarbfeldEncodeError("file-like object doesn't support write() calls")

        outfile.write(b'farbfeld' + pack('<II', self.width, self.height))
        outfile.write(
            array('H', chain(*imageframe))
        .tobytes())
        outfile.flush()

class FarbfeldDecoder:
    "Decoder to decode the Farbfeld image format into 16-bit pixels."

    def __init__(self, infile):
        """
        infile
            a file-like object that must be readable via
            the `read()` call and should return bytes.
        """
        if hasattr(infile, 'read'):
            self.infile = infile
        else:
            raise FarbfeldDecodeError("file-like object doesn't support read() calls")

        if infile.read(8) != b'farbfeld':
            raise FarbfeldDecodeError("invalid signature found while parsing")

        (self.width, self.height) = unpack("<II", infile.read(8))

    def decode(self) -> map:
        """
        Creates a iterable 2D object representing an image frame
        (row-major), pixels are RGBA, bitdepth is 16-bit.
        """
        return map(lambda row: array('H').frombytes(row), iter(self.infile.read(), b''))
