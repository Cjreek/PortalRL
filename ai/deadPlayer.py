from ai.aiClass import AIClass
from random import Random
import esper

from ai import AIClass

class DeadPlayerController(AIClass):
    def process(self, entity, world: esper.World, rng: Random) -> bool:
        return False