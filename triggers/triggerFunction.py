import esper

from game import Game
from components.actor import Actor
from components.level import Level

class TriggerFunction:
    def requiredComponents(self):
        return [Actor]

    def execute(self, game: Game, world: esper.World, level: Level, activatorEntity, triggerEntity):
        return True