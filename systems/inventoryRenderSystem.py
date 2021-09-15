from typing import List
from tcod import Console
import tcod

import guiFunc

from game import Game, GameState
from components import Player, Inventory, InventoryPosition, Position, Item, Input, Trigger, Equipment
from triggers import PickupTrigger
from systems.baseSystem import BaseSystem
from data import layout, colors
from data.enums import EquipmentSlot

class InventoryRenderSystem(BaseSystem):
    def __init__(self, game: Game, console: Console) -> None:
        super().__init__()
        self.game = game
        self.game.registerStateChangeListener(self.gameStateChange)
        self.console = console
        # control
        self.equipmentActive = False
        self.itemIndex = 0

    def gameStateChange(self, newState: GameState):
        if newState == GameState.INVENTORY:
            self.equipmentActive = False
            self.itemIndex = 0

    def canExecute(self, gameState: GameState):
        return gameState in [GameState.INVENTORY]

    def dropItem(self, inventory: Inventory, itemEntry, position: Position):
        item: Item
        itemEntity, item = itemEntry
        inventory.items.remove(itemEntity)
        self.world.remove_component(itemEntity, InventoryPosition)
        self.world.add_component(itemEntity, Position(position.X, position.Y))
        self.world.add_component(itemEntity, Trigger(PickupTrigger()))
        self.game.logMessage(f"Player drops {item.name}")

    def handleInventoryInput(self, equipment: Equipment, inventory: Inventory, itemList: List):
        input: Input
        position: Position
        _, (_, position, input) = self.world.get_components(Player, Position, Input)[0]

        if (input.Up):
            self.itemIndex = max(self.itemIndex - 1, 0)

        elif (input.Down):
            if self.equipmentActive:
                self.itemIndex = min(self.itemIndex + 1, len(EquipmentSlot) - 2)
            else:
                self.itemIndex = min(self.itemIndex + 1, inventory.maxCapacity - 1)

        elif (input.Drop):
            if (not self.equipmentActive) and (self.itemIndex < len(itemList)):
                self.dropItem(inventory, itemList[self.itemIndex], position)

        elif (input.Equip):
            if (self.equipmentActive) and (self.itemIndex < len(EquipmentSlot)-1):
                if (inventory.capacity > 0):
                    (oldItemEntity, _) = equipment.unequip(EquipmentSlot(self.itemIndex))
                    if oldItemEntity:
                        self.world.add_component(oldItemEntity, InventoryPosition(inventory.id))
                        inventory.items.append(oldItemEntity)
                else:
                    self.game.logMessage("You can't carry any more items!")

            elif (not self.equipmentActive) and (self.itemIndex < len(itemList)):
                (oldItemEntity, _) = equipment.equip(itemList[self.itemIndex])
                (equipItemEntity, _) = itemList[self.itemIndex]
                self.world.remove_component(equipItemEntity, InventoryPosition)
                inventory.items.remove(equipItemEntity)
                if (oldItemEntity):
                    self.world.add_component(oldItemEntity, InventoryPosition(inventory.id))
                    inventory.items.append(oldItemEntity)

        elif (input.RawKey == tcod.event.K_TAB):
            self.equipmentActive = not self.equipmentActive
            self.itemIndex = 0
            
        if self.equipmentActive:
            self.itemIndex = max(min(self.itemIndex, len(EquipmentSlot) - 2), 0)
        else:
            self.itemIndex = max(min(self.itemIndex, inventory.maxCapacity - 1), 0)

    def drawEquipmentItem(self, x: int, y: int, slot: EquipmentSlot, item: Item):
        color = colors.WHITE if (self.equipmentActive) and (self.itemIndex == slot.value) else colors.GRAY
        if item:
            guiFunc.printFmt(self.console, x, y, [color, F"{slot.displayName}: ", item.inventoryFg, item.inventoryGlyph + "", color, item.name])
        else:
            self.console.print(x, y, F"{slot.displayName}: -", color)

    def drawInventory(self, equipment: Equipment, inventory: Inventory, itemList: List):
        posX = layout.LEVEL_OFFSET_X + (layout.LEVEL_WIDTH // 2) - (layout.INVENTORY_WIDTH // 2)
        posY = layout.LEVEL_OFFSET_Y +(layout.LEVEL_HEIGHT // 2) - (layout.INVENTORY_HEIGHT // 2)

        guiFunc.drawFrame(self.console, posX, posY, posX + layout.INVENTORY_WIDTH, posY + layout.INVENTORY_HEIGHT, text="Inventory")

        # Equipment
        _, headItem = equipment.getItem(EquipmentSlot.HEAD)
        self.drawEquipmentItem(posX + 30, posY + 3, EquipmentSlot.HEAD, headItem)

        _, bodyItem = equipment.getItem(EquipmentSlot.BODY)
        self.drawEquipmentItem(posX + 30, posY + 4, EquipmentSlot.BODY, bodyItem)

        _, feetItem = equipment.getItem(EquipmentSlot.FEET)
        self.drawEquipmentItem(posX + 30, posY + 5, EquipmentSlot.FEET, feetItem)

        _, mainHand = equipment.getItem(EquipmentSlot.MAINHAND)
        self.drawEquipmentItem(posX + 30, posY + 6, EquipmentSlot.MAINHAND, mainHand)

        _, offHand = equipment.getItem(EquipmentSlot.OFFHAND)
        self.drawEquipmentItem(posX + 30, posY + 7, EquipmentSlot.OFFHAND, offHand)

        # Item List
        n = 0
        item: Item
        for i in range(inventory.maxCapacity):
            _, item = itemList[i] if (i < len(itemList)) else (None, None)
            if (item):
                if (not self.equipmentActive) and (n == self.itemIndex):
                    guiFunc.printFmt(self.console, posX + 2, posY + 3 + n, [colors.WHITE, F"{n+1})", item.inventoryFg, item.inventoryGlyph + "", colors.WHITE, item.name])
                else:
                    guiFunc.printFmt(self.console, posX + 2, posY + 3 + n, [colors.GRAY, F"{n+1})", item.inventoryFg, item.inventoryGlyph + "", colors.GRAY, item.name])
            else:
                if (not self.equipmentActive) and (n == self.itemIndex):
                    self.console.print(posX + 2, posY + 3 + n, F"{n+1})................", colors.WHITE)
                else:
                    self.console.print(posX + 2, posY + 3 + n, F"{n+1})................", colors.GRAY)
            n += 1

    def execute(self, game: Game, *args, **kwargs):
        _, (_, inventory, equipment) = self.world.get_components(Player, Inventory, Equipment)[0]
        
        itemList = list(((entity, item) for entity, (_, item) in self.world.get_components(InventoryPosition, Item)))
        self.handleInventoryInput(equipment, inventory, itemList)
        self.drawInventory(equipment, inventory, itemList)