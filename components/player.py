from __future__ import annotations
from typing import TYPE_CHECKING

import imports
if TYPE_CHECKING:
    from components.actor import Actor
    from actions import Action
    from entity import Entity
    from engine import Engine

class Player(Actor):
    def __init__(self, initiative: int, hitDamage: int, parent: Entity = None) -> None:
        super().__init__(initiative, hitDamage, parent)
    
    def act(self):
        engine: Engine = self.parent.level.engine
        print(self.parent.level)
        if engine.currentState.hasAction():
            action: Action = engine.currentState.getAction()
            action.perform(engine, self.parent)
            return True
        return False