import copy
from typing import List

import esper

from data import renderprio, layout, lighting
from data.enums import Faction
from components import Renderable, Player, Input, FOV, Light, Damageable, Info, Melee, Position, Blocking, AI
from components import Inventory, Equipment, Actor
from ai import RandomMonsterAI, PlayerController, DeadPlayerController

BODY = [Info(name="Body"), Renderable("%", [120,0,0], [0,0,0], renderprio.LOW)]
PLAYER_BODY = [Info(name="Player"), Player(), Actor(1, 1), Input(), AI(DeadPlayerController()), Renderable("%", [180,0,0], [0,0,0], renderprio.HIGH), Damageable(20, None, startHP=0, removeOnDeath=False), FOV(layout.LEVEL_WIDTH // 2), Light((255,0,0), lighting.MAX_LIGHT_LEVEL, False)]

PLAYER = [Info(name="Player", faction=Faction.PLAYER), Player(), Actor(10, 5, startingInitiative=0), Inventory(2), Equipment(), Input(), AI(PlayerController()), Damageable(20, PLAYER_BODY), Melee(3), Blocking(), FOV(layout.LEVEL_WIDTH // 2), Renderable("☻", [255,0,0], [0,0,0], renderprio.HIGH), Light((255,255,0), 8, False)]

SLIME = [Info(name="Slime"), Renderable("o", [0, 180, 0]), Damageable(5, BODY), Melee(1), Actor(20, 5), Blocking(), AI(RandomMonsterAI()), FOV(layout.LEVEL_WIDTH // 2), Light((0,160,0), 6, False)]
SHADOW = [Info(name="Shadow"), Renderable("s", [90, 90, 90]), Damageable(7, BODY), Melee(3), Actor(5, 5), Blocking(), AI(RandomMonsterAI())]

MOBLIST = [SLIME, SHADOW]

def spawn(world: esper.World, mobTemplate: List, x: int, y: int):
    mob = copy.deepcopy(mobTemplate)
    mob.append(Position(x, y))
    return world.create_entity(*mob)
