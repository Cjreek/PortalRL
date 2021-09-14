from components.velocity import Velocity
import esper
from game import Game

class TriggerFunction:
    def requiredComponents(self):
        return [Velocity]

    def execute(self, game: Game, world: esper.World, activatorEntity, triggerEntity):
        pass