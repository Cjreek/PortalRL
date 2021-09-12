import copy
from typing import List

import esper

from data import colors
from components import Position, Renderable, Info, Item, Inventory, InventoryPosition, Trigger
from triggers import PickupTrigger

LEATHER_ARMOR = [Info("Leather Armor"), Item(), Renderable(')', fg=colors.ITEM)]

ITEMPOOL = [LEATHER_ARMOR]

def create(world: esper.World, itemTemplate: List, inventory: Inventory):
    item = copy.deepcopy(itemTemplate)
    item.append(InventoryPosition(inventory.id))
    itemEntity = world.create_entity(*item)
    inventory.items.append(itemEntity)
    return itemEntity

def spawn(world: esper.World, itemTemplate: List, x: int, y: int):
    item = copy.deepcopy(itemTemplate)
    item.append(Position(x, y))
    item.append(Trigger(PickupTrigger()))
    return world.create_entity(*item)