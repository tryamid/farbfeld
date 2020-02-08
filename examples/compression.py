# sample program demonstrating lossless compression with farbfeld image format,
# NOTE: reference software developed by suckless won't support this.

import xz
import farbfeld

out = xz.XZipFile('image0.ff.xz', 'wb')
enc = farbfeld.FarbfeldEncoder(180, 160)

# colors pixels as green with no transparency.
_pix_samp0 = [[0,255,0,255]*enc.width]*enc.height

e.encode(out, _pix_samp0) # pipes xzip with the data output.
out.close()
