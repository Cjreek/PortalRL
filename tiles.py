from typing import Tuple
import numpy

GraphicRec = numpy.dtype([
    ("symbol", numpy.int32),
    ("fg", numpy.double, 3),
    ("bg", numpy.double, 3),
])

TileRec = numpy.dtype([
    ("walkable", numpy.bool),
    ("transparent", numpy.bool),
    ("darkGfx", GraphicRec),
    ("visibleGfx", GraphicRec),
])

def makeTile(*, walkable: int, transparent: int, darkGfx, visibleGfx: Tuple[int, Tuple[float, float, float], Tuple[float, float, float]]) -> numpy.ndarray:
    return numpy.array((walkable, transparent, darkGfx, visibleGfx), dtype=TileRec)

# Tile definitions

shroudGfx = numpy.array((ord(" "), (0, 0, 0), (0, 0, 0)), dtype=GraphicRec)

floor = makeTile(
    walkable=True, 
    transparent=True, 
    darkGfx=(ord("."), (60, 60, 60), (0, 0, 0)),
    visibleGfx=(ord("."), (160, 160, 160), (0, 0, 0)),
)

grass = makeTile(
    walkable=True, 
    transparent=True, 
    darkGfx=(ord("\""), (0, 60, 0), (0, 0, 0)),
    visibleGfx=(ord("\""), (20, 90, 20), (0, 0, 0)),
)

wall = makeTile(
    walkable=False, 
    transparent=False, 
    darkGfx=(ord("#"), (60, 60, 60), (0, 0, 0)),
    visibleGfx=(ord("#"), (160, 160, 160), (0, 0, 0)),
)

floortiles = [floor, grass]