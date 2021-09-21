from tcod import Console
import tcod

import guiFunc

from game import Game, GameState
from components import Player, Inventory, Position, Input, Trigger, Equipment, Level
from triggers import PickupTrigger
from systems.baseSystem import BaseSystem
from data import layout, colors
from data.enums import EquipmentSlot
from data.types import InventoryItem

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

    def dropItem(self, inventory: Inventory, itemEntry: InventoryItem, position: Position):
        inventory.removeItem(itemEntry)
        self.world.add_component(itemEntry.entity, Position(position.X, position.Y))
        self.world.add_component(itemEntry.entity, Trigger(PickupTrigger()))
        self.game.logMessage(f"Player drops {itemEntry.itemData.name}")

    def handleInventoryInput(self, playerPosition: Position, input: Input, equipment: Equipment, inventory: Inventory):
        if (input.Up):
            self.itemIndex = max(self.itemIndex - 1, 0)

        elif (input.Down):
            if self.equipmentActive:
                self.itemIndex = min(self.itemIndex + 1, len(EquipmentSlot) - 2)
            else:
                self.itemIndex = min(self.itemIndex + 1, inventory.maxCapacity - 1)

        elif (input.Drop):
            if (not self.equipmentActive) and (self.itemIndex < len(inventory.items)):
                self.dropItem(inventory, inventory.items[self.itemIndex], playerPosition)

        elif (input.Equip):
            if (self.equipmentActive) and (self.itemIndex < len(EquipmentSlot)-1):
                if (inventory.capacity > 0):
                    oldItem = equipment.unequip(EquipmentSlot(self.itemIndex))
                    if oldItem: inventory.addItem(oldItem)
                else:
                    self.game.logMessage("You can't carry any more items!")
            elif (not self.equipmentActive) and (self.itemIndex < len(inventory.items)):
                oldItem = equipment.equip(inventory.items[self.itemIndex])
                equipItem = inventory.items[self.itemIndex]
                inventory.removeItem(equipItem)
                if (oldItem): inventory.addItem(oldItem)

        elif (input.RawKey == tcod.event.K_TAB):
            self.equipmentActive = not self.equipmentActive
            self.itemIndex = 0
            
        if self.equipmentActive:
            self.itemIndex = max(min(self.itemIndex, len(EquipmentSlot) - 2), 0)
        else:
            self.itemIndex = max(min(self.itemIndex, inventory.maxCapacity - 1), 0)

    def drawEquipmentItem(self, x: int, y: int, slot: EquipmentSlot, item: InventoryItem):
        color = colors.WHITE if (self.equipmentActive) and (self.itemIndex == slot.value) else colors.GRAY
        if item:
            guiFunc.printFmt(self.console, x, y, [color, F"{slot.displayName}: ", item.itemData.inventoryFg, item.itemData.inventoryGlyph + "", color, item.itemData.name])
        else:
            self.console.print(x, y, F"{slot.displayName}: -", color)

    def drawInventory(self, equipment: Equipment, inventory: Inventory):
        posX = layout.LEVEL_OFFSET_X + (layout.LEVEL_WIDTH // 2) - (layout.INVENTORY_WIDTH // 2)
        posY = layout.LEVEL_OFFSET_Y +(layout.LEVEL_HEIGHT // 2) - (layout.INVENTORY_HEIGHT // 2)

        guiFunc.drawFrame(self.console, posX, posY, posX + layout.INVENTORY_WIDTH, posY + layout.INVENTORY_HEIGHT, text="Inventory")

        # Equipment
        headItem = equipment.getItem(EquipmentSlot.HEAD)
        self.drawEquipmentItem(posX + 30, posY + 3, EquipmentSlot.HEAD, headItem)

        bodyItem = equipment.getItem(EquipmentSlot.BODY)
        self.drawEquipmentItem(posX + 30, posY + 4, EquipmentSlot.BODY, bodyItem)

        feetItem = equipment.getItem(EquipmentSlot.FEET)
        self.drawEquipmentItem(posX + 30, posY + 5, EquipmentSlot.FEET, feetItem)

        mainHand = equipment.getItem(EquipmentSlot.MAINHAND)
        self.drawEquipmentItem(posX + 30, posY + 6, EquipmentSlot.MAINHAND, mainHand)

        offHand = equipment.getItem(EquipmentSlot.OFFHAND)
        self.drawEquipmentItem(posX + 30, posY + 7, EquipmentSlot.OFFHAND, offHand)

        # Inventory
        n = 0
        for i in range(inventory.maxCapacity):
            color = colors.WHITE if (not self.equipmentActive) and (self.itemIndex == n) else colors.GRAY
            item = inventory.items[i] if (i < len(inventory.items)) else None
            if (item):
                guiFunc.printFmt(self.console, posX + 2, posY + 3 + n, [color, F"{n+1})", item.itemData.inventoryFg, item.itemData.inventoryGlyph + "", color, item.itemData.name])
            else:
                self.console.print(posX + 2, posY + 3 + n, F"{n+1})................", color)
            n += 1

    def execute(self, game: Game, level: Level):
        _, (_, position, input, inventory, equipment) = self.world.get_components(Player, Position, Input, Inventory, Equipment)[0]
        self.handleInventoryInput(position, input, equipment, inventory)
        self.drawInventory(equipment, inventory)