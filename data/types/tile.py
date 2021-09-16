import numpy

TileGraphic = numpy.dtype([
    ("symbol", numpy.int32),
    ("fg", numpy.double, 3),
    ("bg", numpy.double, 3),
])

Tile = numpy.dtype([
    ("walkable", numpy.bool),
    ("transparent", numpy.bool),
    ("darkGfx", TileGraphic),
    ("visibleGfx", TileGraphic),
])