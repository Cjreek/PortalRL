from components.blocking import Blocking
from typing import Optional
import esper

from components import Position, Velocity, Level, Light, FOV, Damageable, Melee, Renderable, Info

# (Position, Velocity), (Level)
class MovementSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
        self.world: esper.World = self.world

    def entityAt(self, x: int, y: int, blockingOnly: bool = False) -> Optional[int]:
        if blockingOnly:
            return next((entity for entity, (pos, _, _) in self.world.get_components(Position, Renderable, Blocking) if (pos.X == x) and (pos.Y == y)), None)
        else:
            return next((entity for entity, (pos, _) in self.world.get_components(Position, Renderable) if (pos.X == x) and (pos.Y == y)), None)

    def process(self, *args, **kwargs):
        position: Position
        velocity: Velocity
        level: Level
        _, level = self.world.get_component(Level)[0]
        for entity, (position, velocity) in self.world.get_components(Position, Velocity):
            if (velocity.dx != 0) or (velocity.dy != 0):
                destX = position.X + velocity.dx
                destY = position.Y + velocity.dy
                if level.isWalkable(destX, destY):
                    collisionEntity = self.entityAt(destX, destY, True)
                    if not collisionEntity:
                        position.X = destX
                        position.Y = destY
                        if self.world.has_component(entity, FOV):
                            fov = self.world.component_for_entity(entity, FOV)
                            fov.dirty = True
                        if self.world.has_component(entity, Light):
                            light = self.world.component_for_entity(entity, Light)
                            light.dirty = True
                    else:
                        attackerMelee = self.world.try_component(entity, Melee)
                        attackerInfo: Info = self.world.try_component(entity, Info)
                        defenderDamageable = self.world.try_component(collisionEntity, Damageable)
                        defenderInfo: Info = self.world.try_component(collisionEntity, Info)
                        if (attackerMelee) and (defenderDamageable) and (attackerInfo.faction != defenderInfo.faction):
                            defenderDamageable.takeDamage(attackerMelee.damage)