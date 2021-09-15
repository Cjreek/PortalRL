import esper

from rng import RNG
from game import Game

class AIClass:
    def process(self, entity, game: Game, world: esper.World, rng: RNG) -> bool:
        return False