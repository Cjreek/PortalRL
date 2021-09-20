import esper

from rng import RNG
from game import Game
from components.actor import Actor

class AIClass:
    def process(self, entity, actor: Actor, game: Game, world: esper.World, rng: RNG) -> bool:
        return False