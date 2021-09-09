from typing import List
import sound
from data import sfx

class Damageable:
    def __init__(self, maxHP: int, deadEntity: List, startHP: int = None, removeOnDeath: bool = True) -> None:
        self.maxHP = maxHP
        if (startHP is not None):
            self.hp = startHP
        else:
            self.hp = maxHP
        self.removeOnDeath = removeOnDeath
        self.deadEntity = deadEntity
    
    @property
    def isDead(self):
        return self.hp <= 0

    def takeDamage(self, damage: int):
        self.hp -= damage
        sound.play(sfx.HIT)