from typing import Tuple
import numpy

from data.types import Tile, TileGraphic

def makeTile(*, walkable: int, transparent: int, darkGfx, visibleGfx: Tuple[int, Tuple[float, float, float], Tuple[float, float, float]]) -> numpy.ndarray:
    return numpy.array((walkable, transparent, darkGfx, visibleGfx), dtype=Tile)

# Tile definitions

shroudGfx = numpy.array((ord(" "), (0, 0, 0), (0, 0, 0)), dtype=TileGraphic)

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
    visibleGfx=(ord("█"), (160, 160, 160), (0, 0, 0)),
    darkGfx=(ord("█"), (60, 60, 60), (0, 0, 0)),
)

floortiles = [floor, grass]