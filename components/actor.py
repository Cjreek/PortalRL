from __future__ import annotations
from typing import TYPE_CHECKING

import imports
if TYPE_CHECKING:
    from entity import Entity
    from components.component import Component

class Actor(Component):
    def __init__(self, initiative: int, hitDamage: int, parent: Entity = None) -> None:
        super().__init__(parent=parent)
        self.maxInitiative = initiative
        self.initiative = initiative 
        self.hitDamage = hitDamage # anhand von equip berechnen

    def tick(self) -> bool:
        if self.initiative > 0:
            self.initiative -= 1
        
        if (self.initiative == 0): 
            if (self.act()):
                self.initiative = self.maxInitiative
                return True
            else:
                return False
        
        return True

    def act(self):
        pass