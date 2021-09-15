import esper

from game import Game
from components import Velocity

class TriggerFunction:
    def requiredComponents(self):
        return [Velocity]

    def execute(self, game: Game, world: esper.World, activatorEntity, triggerEntity):
        return True