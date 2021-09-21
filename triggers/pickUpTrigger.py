
import esper
from game import Game

from triggers.triggerFunction import TriggerFunction
from components import Info, Inventory, Position, Item, Level
from data.types import InventoryItem

class PickupTrigger(TriggerFunction):
    def requiredComponents(self):
        return [Info, Inventory]

    def execute(self, game: Game, world: esper.World, level: Level, activatorEntity, triggerEntity):
        inventory = world.component_for_entity(activatorEntity, Inventory)
        activatorInfo = world.component_for_entity(activatorEntity, Info)
        triggerInfo = world.component_for_entity(triggerEntity, Info) 
        if len(inventory.items) < inventory.maxCapacity:
            inventory.addItem(InventoryItem(triggerEntity, world.component_for_entity(triggerEntity, Item)))
            world.remove_component(triggerEntity, Position)
            game.logMessage(f"{activatorInfo.name} picks up {triggerInfo.name}")
            return True
        else:
            game.logMessage("You can't carry any more items!")
            return False