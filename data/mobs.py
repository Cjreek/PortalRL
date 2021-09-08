import copy
from typing import List

import esper

from data import renderprio, layout, factions
from components import Renderable, Velocity, Player, Input, FOV, Light, Damageable, Info, Melee, Position, Blocking, AI
from ai import RandomMonsterAI

BODY = [Info(name="Body"), Renderable("%", [120,0,0], [0,0,0], renderprio.LOW)]

PLAYER = [Info(name="Player", faction=factions.PLAYER), Player(), Input(), Damageable(20, BODY), Melee(3), Blocking(), FOV(layout.LEVEL_WIDTH // 2), Velocity(), Renderable("☻", [255,0,0], [0,0,0], renderprio.HIGH), Light((255,255,0), 8, False)]

SLIME = [Info(name="Slime"), Renderable("o", [0, 180, 0]), Damageable(5, BODY), Melee(1), Blocking(), AI(20, RandomMonsterAI()), FOV(layout.LEVEL_WIDTH // 2), Light((0,160,0), 6, False), Velocity()] #Entity("Slime", "o", [0, 180, 0], [DumbMonster(20, 1), Living(5)]) 
SHADOW = [Info(name="Shadow"), Renderable("s", [90, 90, 90]), Damageable(7, BODY), Melee(3), Blocking(), AI(10, RandomMonsterAI()), Velocity()] # Entity("Shadow", "s", [90, 90, 90], [DumbMonster(10, 3), Living(5)]) 

MOBLIST = [SLIME, SHADOW]

def spawn(world: esper.World, mobTemplate: List, x: int, y: int):
    mob = copy.deepcopy(mobTemplate)
    mob.append(Position(x, y))
    return world.create_entity(*mob)
