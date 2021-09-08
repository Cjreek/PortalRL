from typing import List
import sound
from data import sfx

class Damageable:
    def __init__(self, maxHP: int, deadEntity: List) -> None:
        self.maxHP = maxHP
        self.hp = maxHP
        self.deadEntity = deadEntity
    
    @property
    def isDead(self):
        return self.hp <= 0

    def takeDamage(self, damage: int):
        self.hp -= damage
        sound.play(sfx.HIT)