from os import stat


from typing import Tuple
import numpy

from data import layout, lighting

class Light:
    def __init__(self, color: Tuple[int, int, int], intensity: int, static: bool = True) -> None:
        self.color = color
        self.intensity = intensity
        self.static = static
        self.lightMap = numpy.full((layout.LEVEL_WIDTH, layout.LEVEL_HEIGHT), fill_value=lighting.DARKNESS, order="F")
        self.mask = numpy.full((layout.LEVEL_WIDTH, layout.LEVEL_HEIGHT), fill_value=False, order="F")
        self.dirty = True