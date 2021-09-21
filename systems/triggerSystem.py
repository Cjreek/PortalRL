from game import Game
from systems.baseSystem import BaseSystem
from components import Position, Trigger, Actor, Level

class TriggerSystem(BaseSystem):
    def execute(self, game: Game, level: Level):
        activatorPosition: Position
        position: Position
        trigger: Trigger
        for triggerEntity, (position, trigger) in self.world.get_components(Position, Trigger):
            for activatorEntity, (activatorPosition, _) in self.world.get_components(Position, Actor):
                if (activatorPosition.changed) and (position.X == activatorPosition.X) and (position.Y == activatorPosition.Y):
                    if self.world.has_components(activatorEntity, *trigger.triggerObject.requiredComponents()):
                        success = trigger.triggerObject.execute(game, self.world, level, activatorEntity, triggerEntity)
                        if (success and trigger.once):
                            self.world.remove_component(triggerEntity, Trigger)