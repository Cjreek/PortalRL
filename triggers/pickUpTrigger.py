import esper
from game import Game

from triggers.triggerFunction import TriggerFunction
from components import Info, Inventory, Position, InventoryPosition

class PickupTrigger(TriggerFunction):
    def requiredComponents(self):
        return [Info, Inventory]

    def execute(self, game: Game, world: esper.World, activatorEntity, triggerEntity):
        activatorInfo: Info
        triggerInfo: Info
        activatorInfo = world.component_for_entity(activatorEntity, Info)
        inventory = world.component_for_entity(activatorEntity, Inventory)
        triggerInfo = world.component_for_entity(triggerEntity, Info)

        if len(inventory.items) < inventory.maxCapacity:
            inventory.items.append(triggerEntity)
            world.add_component(triggerEntity, InventoryPosition(inventory.id))
            world.remove_component(triggerEntity, Position)
            game.logMessage(f"{activatorInfo.name} picks up {triggerInfo.name}")
            return True
        else:
            game.logMessage("You can't carry any more items!")
            return False