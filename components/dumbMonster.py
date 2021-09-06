from __future__ import annotations
from typing import TYPE_CHECKING

import random

import imports
if TYPE_CHECKING:
    from components.actor import Actor
    from actions import MovementAction

class DumbMonster(Actor):
    def act(self):
        dir = [random.randint(-1, 1), random.randint(-1, 1)] # parent.rng
        action = MovementAction(dir[0], dir[1])
        action.perform(self.parent.level.engine, self.parent)
        return True