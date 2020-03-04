from struct import pack, Struct
from functools import reduce

class FarbfeldEncodeError(Exception):
    pass

class FarbfeldEncoder:
    "Encoder to encode 16-bit pixels into the Farbfeld image format."
    
    def __init__(self, width, height):
        self.width = abs(width)
        self.height = abs(height)

        self._rowutil = Struct(f'<{width * 4}H')

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

        try:
            height = len(imageframe)
            width = int(len(imageframe[0]) / 4)
        except (IndexError, TypeError):
            raise FarbfeldEncodeError("layout of pixels is non-standard")

        if width % 4 != 0:
            raise FarbfeldEncodeError("pixelformat isn't RGBA")

        # slice upto the limit if slice_frame is supplied.
        if self.width > width or self.height > height:
            imageframe = imageframe[:height, :width * 4]
        
        elif self.width < width or self.height < height:
            raise FarbfeldEncodeError(f"pixels supplied is lesser than the amount of pixels specified")

        outfile.write(b'farbfeld' + pack('<II', width, height))
        for row in imageframe:
            outfile.write(self._rowutil.pack(row))
        outfile.flush()
