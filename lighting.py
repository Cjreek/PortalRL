from typing import Tuple
import numpy

LightLevel = numpy.dtype([
    ("color", numpy.double, 3),
    ("level", numpy.byte, 3),
])

def Light(color: Tuple[float, float, float], level: int):
    return numpy.array((color, (level, level, level)), dtype=LightLevel)

DARKNESS = Light([0,0,0], 0)

MAX_LIGHT_LEVEL = 10