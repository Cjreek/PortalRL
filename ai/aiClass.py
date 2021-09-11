from random import Random
import esper

from game import Game

class AIClass:
    def process(self, entity, game: Game, world: esper.World, rng: Random) -> bool:
        return False