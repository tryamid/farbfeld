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
    """
    Encoder to encode raw pixels of an arbitary bitdepth ranging
    `1` bit to `64` bit into Farbfeld image of `16` bit pixels.
    """
    def __init__(self, bitdepth= 8):
        """
        bitdepth
            amount of bits required to represent the input pixels
            in binary (base 2). Pixels not obeying this limit would
            result in quantization in a range.
        """
        if bitdepth < 1 or bitdepth > 64:
            raise FarbfeldEncodeError("bit-depth is beyond allowance")

        self._MAX_BIT_VAL = (2 ** bitdepth) - 1
        self._16B_MAX = 65535

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
        (width, height) = self._wh(imageframe)

        if not hasattr(outfile, 'write'):
            raise FarbfeldEncodeError("file-like object doesn't support write() calls")

        outfile.write(b'farbfeld' + pack('<II', width, height))
        outfile.write(
            array('H',
            map(lambda pix: 
                int(self._maprange(pix, 
                    0, self._MAX_BIT_VAL,
                    0, self._16B_MAX
            )), chain(*imageframe))
        ).tobytes())

        outfile.flush()
    
    @classmethod
    def _wh(cls, imgframe):
        try:
            height = len(imgframe)
            width = int(len(imgframe[0]) / 4)
        except IndexError:
            raise FarbfeldEncodeError("cannot find a valid 2D plane")

        if not width:
            raise FarbfeldEncodeError("cannot find a whole pixel of four-components")

        return (width, height)

    @classmethod
    def _maprange(self, x,a,b,c,d):
	    return c + ((x - a) * (d - b) / (b - a))

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

        if infile.read(8) != b'farbfeld':
            raise FarbfeldDecodeError("invalid signature found while parsing")

        (self.width, self.height) = unpack("<II", infile.read(8))

    def decode(self):
        pass