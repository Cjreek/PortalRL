import esper

from rng import RNG
from game import Game
from ai import AIClass
from components import Velocity

class RandomMonsterAI(AIClass):
    def process(self, entity, game: Game, world: esper.World, rng: RNG):
        velocity: Velocity = world.try_component(entity, Velocity)
        if (velocity):
            velocity.addStep(rng.randint(-1, 1), rng.randint(-1, 1))
            return True