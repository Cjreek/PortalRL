import copy
from typing import List

import esper

from data import layout, lighting
from data.enums import RenderPriority, Faction
from components import Renderable, Velocity, Player, Input, FOV, Light, Damageable, Info, Melee, Position, Blocking, AI
from components import Inventory, Equipment
from ai import RandomMonsterAI, PlayerController, DeadPlayerController

BODY = [Info(name="Body"), Renderable("%", [120,0,0], [0,0,0], RenderPriority.LOW)]
PLAYER_BODY = [Info(name="Player"), Player(), Input(), AI(1, DeadPlayerController()), Renderable("%", [180,0,0], [0,0,0], RenderPriority.HIGH), Damageable(20, None, startHP=0, removeOnDeath=False), FOV(layout.LEVEL_WIDTH // 2), Light((255,0,0), lighting.MAX_LIGHT_LEVEL, False)]

PLAYER = [Info(name="Player", faction=Faction.PLAYER), Player(), Inventory(2), Equipment(), Input(), AI(10, PlayerController(), startsReady=True), Damageable(20, PLAYER_BODY), Melee(3), Blocking(), FOV(layout.LEVEL_WIDTH // 2), Velocity(), Renderable("☻", [255,0,0], [0,0,0], RenderPriority.HIGH), Light((255,255,0), 8, False)]

SLIME = [Info(name="Slime"), Renderable("o", [0, 180, 0]), Damageable(5, BODY), Melee(1), Blocking(), AI(20, RandomMonsterAI()), FOV(layout.LEVEL_WIDTH // 2), Light((0,160,0), 6, False), Velocity()]
SHADOW = [Info(name="Shadow"), Renderable("s", [90, 90, 90]), Damageable(7, BODY), Melee(3), Blocking(), AI(5, RandomMonsterAI()), Velocity()]

MOBLIST = [SLIME, SHADOW]

def spawn(world: esper.World, mobTemplate: List, x: int, y: int):
    mob = copy.deepcopy(mobTemplate)
    mob.append(Position(x, y))
    return world.create_entity(*mob)
