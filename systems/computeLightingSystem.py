import math
import numpy

from game import Game
from systems.baseSystem import BaseSystem
from components import Position, Light, FOV, Player
from data import layout, colors
                    
# (Level), (Position, FOV, Light)
class ComputeLightingSystem(BaseSystem):

    def calculateLighting(self, position: Position, light: Light, fov: FOV):
        for x in range(-light.intensity+1, light.intensity):
            for y in range(-light.intensity+1, light.intensity):
                targetX = position.X + x
                targetY = position.Y + y
                if (targetX >= 0) and (targetX < layout.LEVEL_WIDTH) and (targetY >= 0) and (targetY < layout.LEVEL_HEIGHT) and (fov.fov[targetX, targetY]):
                    d = int(round(math.dist([targetX, targetY], [position.X, position.Y])))
                    if d < light.intensity:
                        light.mask[targetX, targetY] = True
                        light.lightMap["color"][targetX, targetY] = light.color
                        light.lightMap["level"][targetX, targetY] = light.intensity -  d

    def execute(self, game: Game, *args, **kwargs):
        position: Position
        fov: FOV
        light: Light
        playerFov: FOV
        _, (_, playerFov) = self.world.get_components(Player, FOV)[0]
        for _, (position, fov, light) in self.world.get_components(Position, FOV, Light):
            if (light.dirty):
                light.lightMap["color"] = colors.WHITE
                light.lightMap["level"] = 0
                light.mask[:] = False
                fovIntersection = playerFov.fov & fov.lightFov
                if numpy.any(fovIntersection):
                    self.calculateLighting(position, light, fov)
                light.dirty = False