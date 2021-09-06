from __future__ import annotations
from typing import TYPE_CHECKING

import imports
if TYPE_CHECKING:
    from components.damageable import Living
    from components.lightsource import LightSource
    from components.dumbMonster import DumbMonster
    from entity import Entity

SLIME = Entity("Slime", "o", [0, 180, 0], [DumbMonster(20, 1), Living(5), LightSource((0,160,0), False, 6)]) 
SHADOW = Entity("Shadow", "s", [90, 90, 90], [DumbMonster(10, 3), Living(5)]) 

MOBLIST = [SLIME, SHADOW]