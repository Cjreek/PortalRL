import copy
from typing import List

import esper

from data import colors
from data.enums import EquipmentSlot
from components import Position, Renderable, Info, Item, Trigger
from triggers import PickupTrigger

LEATHER_ARMOR = [Info("Leather Armor"), Item("Leather Armor", "()", EquipmentSlot.BODY), Renderable(')', fg=colors.ITEM)]
LONGSWORD = [Info("Longsword"), Item("Longsword", "┼─", EquipmentSlot.MAINHAND), Renderable('/', fg=colors.ITEM)]

ITEMPOOL = [LEATHER_ARMOR, LONGSWORD]

def create(world: esper.World, itemTemplate: List):
    item = copy.deepcopy(itemTemplate)
    itemEntity = world.create_entity(*item)
    return itemEntity

def spawn(world: esper.World, itemTemplate: List, x: int, y: int):
    item = copy.deepcopy(itemTemplate)
    item.append(Position(x, y))
    item.append(Trigger(PickupTrigger()))
    return world.create_entity(*item)