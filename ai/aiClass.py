import esper

from rng import RNG
from game import Game
from components.actor import Actor
from components.level import Level

class AIClass:
    def process(self, entity, actor: Actor, level: Level, game: Game, world: esper.World, rng: RNG) -> bool:
        return False