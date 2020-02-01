import farbfeld
from array import array

pixbuf = [[255] * 16 * 4] * 16

fe = farbfeld.FarbfeldEncoder(16, 16)
fe.encode(open('t01.ff', 'wb'), pixbuf)

fd = farbfeld.FarbfeldDecoder(open('t01.ff', 'rb'))
pixbuf1 = list(fd.decode())

# ensure all the pixels are same as the input.
for y in range(16):
    for x in range(16):
        for p in range(4):
            assert pixbuf[y][x+p] == pixbuf1[y][x+p]