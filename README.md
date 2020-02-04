![](https://i.imgur.com/m6bVkrs.png)

[![PyPI](https://img.shields.io/pypi/v/py-farbfeld?style=flat-square)](https://pypi.org/project/py-farbfeld/)

A Python module for encoding and decoding [Farbeld image format][1]. It encodes or decodes pixels of
16-bit per pixel in the big-endian byteorder in the [**RGBA** pixel-format][2]. This module provides
a simple but elegant API.

### FAQ
**Can it encode or decode compressed image data?**
<br/>
Data compression on the image is not specified in the specification
so as this *API*. If a compression is applied externally, it must be
decoded before this library can parse it.

> The code is platform independent and requires no external dependencies. Python *`>=3.5`* is required
for runtime.

[1]: https://tools.suckless.org/farbfeld/
[2]: https://en.wikipedia.org/wiki/RGBA_color_mod
