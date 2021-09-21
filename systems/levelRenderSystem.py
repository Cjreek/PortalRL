import numpy
import copy

from tcod import Console

from game import Game
from systems.baseSystem import BaseSystem
from components import Level, Player, FOV, Light
from data import tiles, colors, lighting

# (Player, FOV)
class LevelRenderSystem(BaseSystem):
    def __init__(self, console: Console, posX: int, posY: int) -> None:
        super().__init__()
        self.console = console
        self.posX = posX
        self.posY = posY

    def updateLighting(self, lightmap):
        light: Light
        lightmap["level"] = 0
        lightmap["color"] = colors.WHITE
        for _, light in self.world.get_component(Light):
            totalLevel = lightmap["level"] + light.lightMap["level"]
            lightmap["color"][light.mask] = (lightmap["color"][light.mask] * (lightmap["level"][light.mask] / totalLevel[light.mask])[:, None]) + (light.lightMap["color"][light.mask] * (light.lightMap["level"][light.mask] / totalLevel[light.mask])[:, None])
            lightmap["level"][light.mask] = numpy.minimum(lightmap["level"][light.mask] + light.lightMap["level"][light.mask], lighting.MAX_LIGHT_LEVEL)

    def applyLighting(self, tiles, lightmap):
        tiles["fg"] = ((tiles["fg"] + lightmap["color"]) / 2) * (lightmap["level"] / lighting.MAX_LIGHT_LEVEL)[:,:, None]

    def execute(self, game: Game, level: Level): 
        playerFOV: FOV
        _, (_, playerFOV) = self.world.get_components(Player, FOV)[0]

        sliceX = slice(self.posX, self.posX + level.width)
        sliceY = slice(self.posY, self.posY + level.height)

        if game.showMap:
            selectedTiles = copy.deepcopy(level.tiles["visibleGfx"])
        else:
            selectedTiles = numpy.select(condlist=[playerFOV.fov], choicelist=[level.tiles["visibleGfx"]], default=tiles.shroudGfx)

        # lighting
        if game.useLighting:
            self.updateLighting(level.lightmap)
            self.applyLighting(selectedTiles, level.lightmap)

        self.console.tiles_rgb[sliceX, sliceY] = selectedTiles