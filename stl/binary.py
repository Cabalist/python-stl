
import struct
from stl.types import *


class Reader(object):

    def __init__(self, file):
        self.file = file
        self.offset = 0

    def read_bytes(self, byte_count):
        bytes = self.file.read(byte_count)
        if len(bytes) < byte_count:
            raise FormatError(
                "Unexpected end of file at offset %i" % (
                    self.offset + len(bytes),
                )
            )
        self.offset += byte_count
        return bytes

    def read_uint32(self):
        bytes = self.read_bytes(4)
        return struct.unpack('<I', bytes)[0]

    def read_uint16(self):
        bytes = self.read_bytes(2)
        return struct.unpack('<H', bytes)[0]

    def read_float(self):
        bytes = self.read_bytes(4)
        return struct.unpack('<f', bytes)[0]

    def read_vector3d(self):
        x = self.read_float()
        y = self.read_float()
        z = self.read_float()
        return Vector3d(x, y, z)


class FormatError(ValueError):
    pass


def parse(file):
    r = Reader(file)

    ret = Solid()

    # Skip the header
    r.read_bytes(80)

    num_facets = r.read_uint32()

    for i in xrange(0, num_facets):
        normal = r.read_vector3d()
        vertices = tuple(
            r.read_vector3d() for j in xrange(0, 3)
        )
        ret.add_facet(
            normal=normal,
            vertices=vertices,
        )
        attr_byte_count = r.read_uint16()
        if attr_byte_count > 0:
            # skip attribute bytes
            r.read_bytes(attr_byte_count)

    return ret
