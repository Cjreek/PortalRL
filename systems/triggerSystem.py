from components.velocity import Velocity
from game import Game
from systems.baseSystem import BaseSystem
from components import Position, Trigger

class TriggerSystem(BaseSystem):
    def execute(self, game: Game, *args, **kwargs):
        activatorPosition: Position
        position: Position
        trigger: Trigger
        for triggerEntity, (position, trigger) in self.world.get_components(Position, Trigger):
            for activatorEntity, (activatorPosition, _) in self.world.get_components(Position, Velocity):
                if (position.X == activatorPosition.X) and (position.Y == activatorPosition.Y):
                    if self.world.has_components(activatorEntity, *trigger.triggerObject.requiredComponents()):
                        trigger.triggerObject.execute(game, self.world, activatorEntity, triggerEntity)
                        if (trigger.once):
                            self.world.remove_component(triggerEntity, Trigger)