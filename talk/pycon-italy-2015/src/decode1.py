import sys
import struct

P1 = '\x0c\x00\x00\x00"\x00\x00\x00\x07\x00'
P2 = '\x15\x00\x00\x00+\x00\x00\x00\x08\x00'

PLIST = [P1, P2] * 2000

class Field(object):

    def __init__(self, fmt, offset):
        self.fmt = fmt
        self.offset = offset


class Message(object):

    def __init__(self, name, fields):
        self._name = name
        self._fields = fields

    def read(self, buf, name):
        f = self._fields[name]
        return struct.unpack_from(f.fmt, buf, f.offset)[0]


Point = Message('Point', {
    'x': Field('l', 0),
    'y': Field('l', 4),
    'color': Field('i', 8)
    })


def main():
    res = 0
    for p in PLIST:
        x = Point.read(p, 'x')
        res += x
    print res

main()
