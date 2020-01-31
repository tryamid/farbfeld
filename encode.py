from array import array
from struct import pack
from itertools import chain

class FarbfeldEncodeError(Exception):
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
