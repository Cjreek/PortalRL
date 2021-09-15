from typing import Optional

from game import Game
from systems.baseSystem import BaseSystem
from components import Position, Velocity, Level, Light, FOV, Damageable, Melee, Renderable, Info, Blocking

# (Position, Velocity), (Level)
class MovementSystem(BaseSystem):
    def entityAt(self, x: int, y: int, blockingOnly: bool = False) -> Optional[int]:
        if blockingOnly:
            return next((entity for entity, (pos, _, _) in self.world.get_components(Position, Renderable, Blocking) if (pos.X == x) and (pos.Y == y)), None)
        else:
            return next((entity for entity, (pos, _) in self.world.get_components(Position, Renderable) if (pos.X == x) and (pos.Y == y)), None)

    def moveEntity(self, entity, position: Position, destX: int, destY: int):
        position.X = destX
        position.Y = destY
        position.changed = True
        if self.world.has_component(entity, FOV):
            fov = self.world.component_for_entity(entity, FOV)
            fov.dirty = True
        if self.world.has_component(entity, Light):
            light = self.world.component_for_entity(entity, Light)
            light.dirty = True
    
    def doEntityMeleeAttack(self, game: Game, attackerEntity, defenderEntity):
        attackerMelee = self.world.try_component(attackerEntity, Melee)
        attackerInfo: Info = self.world.try_component(attackerEntity, Info)
        defenderDamageable = self.world.try_component(defenderEntity, Damageable)
        defenderInfo: Info = self.world.try_component(defenderEntity, Info)
        if (attackerMelee) and (defenderDamageable) and (attackerInfo.faction != defenderInfo.faction):
            defenderDamageable.takeDamage(attackerMelee.damage)
            game.logMessage(f"{attackerInfo.name} hits {defenderInfo.name} for {attackerMelee.damage}")
            if defenderDamageable.isDead:
                game.logMessage(f"{attackerInfo.name} kills {defenderInfo.name}")


    def execute(self, game: Game, *args, **kwargs):
        position: Position
        velocity: Velocity
        level: Level
        _, level = self.world.get_component(Level)[0]
        for entity, (position, velocity) in self.world.get_components(Position, Velocity):
            position.changed = False
            for step in velocity.steps:
                destX = position.X + step.dx
                destY = position.Y + step.dy
                if level.isWalkable(destX, destY):
                    collisionEntity = self.entityAt(destX, destY, True)
                    if not collisionEntity:
                        self.moveEntity(entity, position, destX, destY)
                    else:
                        self.doEntityMeleeAttack(game, entity, collisionEntity)
                velocity.steps.remove(step)