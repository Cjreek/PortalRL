from __future__ import annotations
from typing import TYPE_CHECKING

from math import dist
from typing import Tuple

import numpy
from tcod.map import compute_fov

import imports
if TYPE_CHECKING:
    import layout
    from imports import components
    # from components.component import Component
    import lighting

class LightSource(components.Component):
    def __init__(self, colorRGB: Tuple[int, int, int], static: bool, level: int = lighting.MAX_LIGHT_LEVEL, parent = None) -> None:
        super().__init__(tickAlways=True, parent=parent)
        self.color = colorRGB
        self.level = min(level, lighting.MAX_LIGHT_LEVEL)
        self.lightMap = numpy.full((layout.LEVEL_WIDTH, layout.LEVEL_HEIGHT), fill_value=lighting.DARKNESS, order="F")
        self.mask = numpy.full((layout.LEVEL_WIDTH, layout.LEVEL_HEIGHT), fill_value=False, order="F")
        self.static = static
        self.fov = []
        self.__lastParentPos = [-1, -1]

    def beforeRender(self):
        self.update()

    def update(self):
        if (self.static and (len(self.fov) == 0)) or (self.__lastParentPos[0] != self.parent.x) or (self.__lastParentPos[1] != self.parent.y):
            self.__lastParentPos = [self.parent.x, self.parent.y]

            self.fov = compute_fov(self.parent.level.tiles["transparent"], (self.parent.x, self.parent.y), radius=layout.LEVEL_WIDTH // 2)

            self.lightMap["color"] = (255,255,255)
            self.lightMap["level"] = (0, 0, 0)
            self.mask[:] = False
            for x in range(-self.level+1, self.level):
                for y in range(-self.level+1, self.level):
                    targetX = self.parent.x + x
                    targetY = self.parent.y + y
                    if (targetX >= 0) and (targetX < layout.LEVEL_WIDTH) and (targetY >= 0) and (targetY < layout.LEVEL_HEIGHT) and (self.fov[targetX, targetY]): #and ((self.parent == self.parent.level.player) or (self.parent.level.player.fov[targetX, targetY])):
                        d = int(round(dist([targetX, targetY], [self.parent.x, self.parent.y])))
                        if d < self.level:
                            self.mask[targetX, targetY] = True
                            self.lightMap["color"][targetX, targetY] = self.color
                            self.lightMap["level"][targetX, targetY] = (self.level - d, self.level - d, self.level - d)

            
                        
            