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
from itertools import chain, zip_longest

class FarbfeldEncodeError(Exception):
    pass

class FarbfeldDecodeError(Exception):
    pass

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

class FarbfeldEncoder:
    """
    Encoder to encode raw pixels of an arbitary bitdepth ranging
    `1` bit to `64` bit into Farbfeld image of `16` bit pixels.
    """
    def __init__(self, width, height):
        self.width = abs(width)
        self.height = abs(height)

    def encode(self, outfile, imageframe):
        """
        outfile
            a file-like object that supports write() calls and
            support bytes as the first argument.

        imageframe
            a subscriptable 2D object, that must have one element
            at the top-level, inside an element must contain
            4 elements (sub-pixels). Pixel must be ordered as 'RGBA'.
        """
        if not hasattr(outfile, 'write'):
            raise FarbfeldEncodeError("file-like object doesn't support write() calls")

        outfile.write(b'farbfeld' + pack('<II', self.width, self.height))
        outfile.write(
            array('H', chain(*imageframe))
        .tobytes())
        outfile.flush()

class FarbfeldDecoder:
    """
    Decoder to decode the Farbfeld image format into raw pixels of
    `16` bit into an arbitary bitdepth ranging `1` bit to `64` bits.
    """
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

    def decode(self):
        return array('H', [iter(self.infile.read(), b'')])
