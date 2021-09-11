from math import dist
import numpy

from game import Game
from systems.baseSystem import BaseSystem
from components import Position, Light, FOV, Player
from data import layout

# (Level), (Position, FOV, Light)
class ComputeLightingSystem(BaseSystem):
    def execute(self, game: Game, *args, **kwargs):
        position: Position
        fov: FOV
        light: Light
        playerFov: FOV
        _, (_, playerFov) = self.world.get_components(Player, FOV)[0]
        for _, (position, fov, light) in self.world.get_components(Position, FOV, Light):
            if (light.dirty):
                light.lightMap["color"] = (255,255,255)
                light.lightMap["level"] = (0, 0, 0)
                light.mask[:] = False

                fovIntersection = playerFov.fov & fov.lightFov
                if numpy.any(fovIntersection):
                    for x in range(-light.intensity+1, light.intensity):
                        for y in range(-light.intensity+1, light.intensity):
                            targetX = position.X + x
                            targetY = position.Y + y
                            if (targetX >= 0) and (targetX < layout.LEVEL_WIDTH) and (targetY >= 0) and (targetY < layout.LEVEL_HEIGHT) and (fov.fov[targetX, targetY]): #and ((self.parent == self.parent.level.player) or (self.parent.level.player.fov[targetX, targetY])):
                                d = int(round(dist([targetX, targetY], [position.X, position.Y])))
                                if d < light.intensity:
                                    light.mask[targetX, targetY] = True
                                    light.lightMap["color"][targetX, targetY] = light.color
                                    light.lightMap["level"][targetX, targetY] = (light.intensity - d, light.intensity - d, light.intensity - d)
                light.dirty = False