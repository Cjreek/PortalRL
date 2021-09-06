from __future__ import annotations
from typing import TYPE_CHECKING

from typing import Tuple, List
from random import Random

import numpy
from tcod.console import Console

import imports
if TYPE_CHECKING:
    import layout
    import tiles
    import lighting
    from components.lightsource import LightSource
    from entity import Entity
    from engine import Engine
    from gamestates.game import Game

class Level:
    def __init__(self, engine: Engine, game: Game, seed: int) -> None:
        self.engine = engine
        self.game = game
        self.entities: List[Entity] = []
        self.tiles = numpy.full((layout.LEVEL_WIDTH, layout.LEVEL_HEIGHT), fill_value=tiles.wall, order="F")
        self.lighting = numpy.full((layout.LEVEL_WIDTH, layout.LEVEL_HEIGHT), fill_value=lighting.DARKNESS, order="F")
        self.explored = numpy.full((layout.LEVEL_WIDTH, layout.LEVEL_HEIGHT), fill_value=False, order="F")
        self.seed = seed
        self.rng: Random = Random(self.seed)
        self.rooms = []

        self.__maxLevelLighting = numpy.full((layout.LEVEL_WIDTH, layout.LEVEL_HEIGHT, 3), fill_value=[lighting.MAX_LIGHT_LEVEL,lighting.MAX_LIGHT_LEVEL, lighting.MAX_LIGHT_LEVEL], order="F")

    @property
    def width(self) -> int:
        return layout.LEVEL_WIDTH

    @property
    def height(self) -> int:
        return layout.LEVEL_HEIGHT

    @property
    def player(self) -> Entity:
        return self.game.player

    def addEntity(self, entity: Entity):
        entity.level = self
        self.entities.append(entity)

    def removeEntity(self, entity: Entity):
        entity.level = None
        self.entities.remove(entity)

    def entityAt(self, x: int, y: int, collidableOnly: bool) -> Entity:
        return next((entity for entity in self.entities if (entity.x == x) and (entity.y == y) and ((entity.hasCollider) or (not collidableOnly))), None)

    def isWalkable(self, x,y: int) -> bool:
        return self.tiles["walkable"][x, y]

    def isTransparent(self, x,y: int) -> bool:
        return self.tiles["transparent"][x, y]

    def isVisible(self, x: int, y: int) -> bool:
        return self.player.fov[x, y]
        # return self.visible[x, y]

    def print(self, console: Console, x: int, y: int, string: str, fg: Tuple[int, int, int] = [255, 255, 255]):
        console.print(x=layout.LEVEL_OFFSET_X + x, y=layout.LEVEL_OFFSET_Y + y, string=string, fg=fg)

    def updateLighting(self):
        self.lighting["level"] = (0,0,0)
        self.lighting["color"] = (0,0,0)
        for entity in self.entities:
            lightComp: LightSource = entity.getComponent(LightSource)
            if lightComp:
                totalLevel = self.lighting["level"] + lightComp.lightMap["level"]
                self.lighting["color"][lightComp.mask] = (self.lighting["color"][lightComp.mask] * (self.lighting["level"][lightComp.mask] / totalLevel[lightComp.mask])) + (lightComp.lightMap["color"][lightComp.mask] * (lightComp.lightMap["level"][lightComp.mask] / totalLevel[lightComp.mask]))
                self.lighting["level"][lightComp.mask] = numpy.minimum(self.lighting["level"][lightComp.mask] + lightComp.lightMap["level"][lightComp.mask], self.__maxLevelLighting[lightComp.mask])

    def applyLighting(self, tiles):
        tiles["fg"] = ((tiles["fg"] + self.lighting["color"]) / 2) * self.lighting["level"] / lighting.MAX_LIGHT_LEVEL
        # tiles["fg"] = tiles["fg"] * self.lighting["level"] / lighting.MAX_LIGHT_LEVEL

        # # langsam aber besser
        # for x in range(len(tiles["fg"])):
        #     for c in range(len(tiles["fg"][x])):
        #         if self.isVisible(x, c):
        #             tiles["fg"][x, c] = color.toHLS((tiles["fg"][x, c] + self.lighting["color"][x, c]) / 2)
        #             tiles["fg"][x, c, 1] = tiles["fg"][x, c, 1] * (self.lighting["level"][x, c][0] / lighting.MAX_LIGHT_LEVEL)
        #             tiles["fg"][x, c] = color.toRGB(tiles["fg"][x, c])

        return tiles
    
    def beforeRender(self):
        for entity in self.entities:
            entity.beforeRender()

    def render(self, console: Console) -> None:
        self.beforeRender()

        sliceX = slice(layout.LEVEL_OFFSET_X, layout.LEVEL_OFFSET_X + layout.LEVEL_WIDTH)
        sliceY = slice(layout.LEVEL_OFFSET_Y, layout.LEVEL_OFFSET_Y + layout.LEVEL_HEIGHT)

        selectedTiles = numpy.select(condlist=[self.player.fov, self.explored], choicelist=[self.tiles["visibleGfx"], self.tiles["darkGfx"]], default=tiles.shroudGfx)
        
        if self.engine.useLighting:
            self.updateLighting()
            selectedTiles = self.applyLighting(selectedTiles)

        console.tiles_rgb[sliceX, sliceY] = selectedTiles

        self.entities.sort(key=lambda entity: entity.renderPrio)
        for entity in self.entities:
            if (self.isVisible(entity.x, entity.y)):
                entity.render(console)

    def tick(self):
        while (self.player.actor.initiative > 0) and (self.player in self.entities):
            for entity in self.entities:       
                entity.tick()
        
        if self.player.actor.initiative == 0:
            self.player.tick()