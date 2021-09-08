from ai.aiClass import AIClass
from random import Random
import esper

from ai import AIClass

from components import Velocity

class RandomMonsterAI(AIClass):
    def process(self, entity, world: esper.World, rng: Random):
        velocity: Velocity = world.try_component(entity, Velocity)
        if (velocity):
            velocity.dx = rng.randint(-1, 1)
            velocity.dy = rng.randint(-1, 1)