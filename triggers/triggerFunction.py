import esper

from game import Game
from components.actor import Actor

class TriggerFunction:
    def requiredComponents(self):
        return [Actor]

    def execute(self, game: Game, world: esper.World, activatorEntity, triggerEntity):
        return True