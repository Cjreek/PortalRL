from __future__ import annotations
from typing import TYPE_CHECKING

from pygame.mixer import Sound

import imports
if TYPE_CHECKING:
    import renderprio
    from entity import Entity
    from components.component import Component

class Damageable(Component):
    def __init__(self, maxHP: int) -> None:
        super().__init__()
        self.maxHP = maxHP
        self.hp = maxHP
    
    def getDeadEntity(self):
        return None

    def isDead(self):
        return self.hp <= 0

    def takeDamage(self, damage: int):
        self.hp -= damage

        hitSound: Sound = Sound("data\\hit.wav")
        hitSound.play(0)

        if self.isDead():
            deadEntity: Entity = self.getDeadEntity()
            if (deadEntity):
                deadEntity.x, deadEntity.y = self.parent.x, self.parent.y
                self.parent.level.addEntity(deadEntity)
            self.parent.level.removeEntity(self.parent)

class Living(Damageable):
    def getDeadEntity(self):
        return Entity("body", "%", [180, 0, 0], hasCollider=False, renderPrio=renderprio.LOW)

class Breakable(Damageable):
    pass