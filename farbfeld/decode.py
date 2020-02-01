from struct import unpack, iter_unpack

class FarbfeldDecodeError(Exception):
    pass

class FarbfeldDecoder:
    "Decoder to decode the Farbfeld image format into 16-bit pixels."

    def __init__(self, infile):
        """
        infile
            a file-like object that must be readable via
            the `read()` call and should return bytes.
        """
        if hasattr(infile, 'read'):
            self._infile = infile
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
        return map(lambda row: map(lambda pix: pix[0], iter_unpack('<H', row)), 
                    iter(lambda: self._infile.read(self.width * 4), b''))
