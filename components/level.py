from typing import Tuple
import numpy

from rng import RNG
from data import tiles, lighting

class Level:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.seed = seed
        self.rng: RNG = None
        self.width = width
        self.height = height
        self.tiles = numpy.full((self.width, self.height), fill_value=tiles.wall, order="F")
        self.lightmap = numpy.full((self.width, self.height), fill_value=lighting.DARKNESS, order="F")
        self.entities = {}
        self.blockingEntities = {}
        self.rooms = []
        self.setSeed(seed)
    
    def setSeed(self, seed):
        self.seed = seed
        self.rng = RNG(self.seed)

    def entitiesAt(self, x: int, y: int, onlyBlocking: bool = False):
        if onlyBlocking:
            return self.blockingEntities.get((x, y), [])
        else:
            return self.entities.get((x, y), [])

    def reportEntityMovement(self, entity, oldPos: Tuple[int, int], newPos: Tuple[int, int]):       
        self.entities[oldPos].remove(entity)
        if not (newPos in self.entities):
            self.entities[newPos] = [entity]
        else:
            self.entities[newPos].append(entity)

        if (oldPos in self.blockingEntities) and (entity in self.blockingEntities[oldPos]):
            self.blockingEntities[oldPos].remove(entity)
            if not (newPos in self.blockingEntities):
                self.blockingEntities[newPos] = [entity]
            else:
                self.blockingEntities[newPos].append(entity)

    def isWalkable(self, x: int, y: int) -> bool:
        return self.tiles["walkable"][x, y]

    def isTransparent(self, x: int, y: int) -> bool:
        return self.tiles["transparent"][x, y]
        