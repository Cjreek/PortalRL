from __future__ import annotations
from typing import TYPE_CHECKING

import tcod.event

import imports
if TYPE_CHECKING:
    import generation
    from components.damageable import Damageable
    from gamestates.game import Game
    from engine import Engine
    from entity import Entity
    from components.actor import Actor
    
class Action:
    def perform(self, engine: Engine, entity: Entity):
        pass

class DebugAction:
    def __init__(self, key) -> None:
        self.key = key

    def perform(self, engine: Engine, entity: Entity):
        if self.key == tcod.event.K_F2:
            engine.useLighting = not engine.useLighting
        if self.key == tcod.event.K_F5:
            engine.level = generation.generateLevel(5, 10, 10, 20, engine)

class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity):
        if isinstance(engine.currentState, Game):
            game: game.Game = engine.currentState
            destX, destY = entity.x + self.dx, entity.y + self.dy
            if game.level.isWalkable(destX, destY):
                collEntity = game.level.entityAt(destX, destY, True)
                if (collEntity) and not (collEntity == entity) and (collEntity.faction != entity.faction):
                    selfActor: Actor = entity.actor
                    otherHurt: Damageable = collEntity.getComponent(Damageable)
                    if (selfActor and otherHurt):
                        otherHurt.takeDamage(selfActor.hitDamage)
                    else:
                        print("Da ist ein " + collEntity.name + "!")
                else:
                    entity.move(self.dx, self.dy)

class CancelAction(Action):
    def perform(self, engine: Engine, entity: Entity):
        raise SystemExit()