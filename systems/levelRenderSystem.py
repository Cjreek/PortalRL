import esper
import numpy
import copy

from tcod import Console

from gamestate import Game
from data import tiles, layout, lighting
from components import Level, Player, FOV, Light

# (Level), (Player, FOV)
class LevelRenderSystem(esper.Processor):
    def __init__(self, console: Console, posX: int, posY: int) -> None:
        super().__init__()
        self.console = console
        self.posX = posX
        self.posY = posY
        self.world: esper.World = self.world
        self.__maxLevelLighting = numpy.full((layout.LEVEL_WIDTH, layout.LEVEL_HEIGHT, 3), fill_value=[lighting.MAX_LIGHT_LEVEL,lighting.MAX_LIGHT_LEVEL, lighting.MAX_LIGHT_LEVEL], order="F")

    def updateLighting(self, lightmap):
        light: Light
        lightmap["level"] = (0,0,0)
        lightmap["color"] = (255,255,255)
        for _, light in self.world.get_component(Light):
            totalLevel = lightmap["level"] + light.lightMap["level"]
            lightmap["color"][light.mask] = (lightmap["color"][light.mask] * (lightmap["level"][light.mask] / totalLevel[light.mask])) + (light.lightMap["color"][light.mask] * (light.lightMap["level"][light.mask] / totalLevel[light.mask]))
            lightmap["level"][light.mask] = numpy.minimum(lightmap["level"][light.mask] + light.lightMap["level"][light.mask], self.__maxLevelLighting[light.mask])

    def applyLighting(self, tiles, lightmap):
        tiles["fg"] = ((tiles["fg"] + lightmap["color"]) / 2) * lightmap["level"] / lighting.MAX_LIGHT_LEVEL

    def process(self, *args, **kwargs): 
        level: Level
        playerFOV: FOV
        game: Game = kwargs["game"]
        _, (_, playerFOV) = self.world.get_components(Player, FOV)[0]
        for _, level in sorted(self.world.get_component(Level)):

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