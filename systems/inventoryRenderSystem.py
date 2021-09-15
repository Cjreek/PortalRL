from typing import List
from tcod import Console

import guiFunc

from game import Game, GameState
from components import Player, Inventory, InventoryPosition, Position, Item, Input, Trigger
from triggers import PickupTrigger
from systems.baseSystem import BaseSystem
from data import layout, colors

class InventoryRenderSystem(BaseSystem):
    def __init__(self, game: Game, console: Console) -> None:
        super().__init__()
        self.game = game
        self.game.registerStateChangeListener(self.gameStateChange)
        self.console = console
        # control
        self.itemIndex = 0

    def gameStateChange(self, newState: GameState):
        if newState == GameState.INVENTORY:
            self.itemIndex = 0

    def canExecute(self, gameState: GameState):
        return gameState in [GameState.INVENTORY]

    def dropItem(self, inventory: Inventory, itemEntry, position: Position):
        item: Item
        itemEntity, (_, item) = itemEntry
        inventory.items.remove(itemEntity)
        self.world.remove_component(itemEntity, InventoryPosition)
        self.world.add_component(itemEntity, Position(position.X, position.Y))
        self.world.add_component(itemEntity, Trigger(PickupTrigger()))
        self.game.logMessage(f"Player drops {item.name}")

    def handleInventoryInput(self, inventory: Inventory, itemList: List):
        input: Input
        position: Position
        _, (_, position, input) = self.world.get_components(Player, Position, Input)[0]
        if (input.Up):
            self.itemIndex = max(self.itemIndex - 1, 0)
        elif (input.Down):
            self.itemIndex = min(self.itemIndex + 1, inventory.maxCapacity - 1)
        elif (input.Drop):
            if self.itemIndex < len(itemList):
                self.dropItem(inventory, itemList[self.itemIndex], position)
            
        self.itemIndex = max(min(self.itemIndex, inventory.maxCapacity - 1), 0)

    def drawInventory(self, inventory: Inventory, itemList: List):
        posX = layout.LEVEL_OFFSET_X + (layout.LEVEL_WIDTH // 2) - (layout.INVENTORY_WIDTH // 2)
        posY = layout.LEVEL_OFFSET_Y +(layout.LEVEL_HEIGHT // 2) - (layout.INVENTORY_HEIGHT // 2)

        guiFunc.drawFrame(self.console, posX, posY, posX + layout.INVENTORY_WIDTH, posY + layout.INVENTORY_HEIGHT, text="Inventory")

        n = 0
        item: Item
        for i in range(inventory.maxCapacity):
            _, (_, item) = itemList[i] if (i < len(itemList)) else (None, (None, None))
            if (item):
                if (n == self.itemIndex):
                    guiFunc.printFmt(self.console, posX + 30, posY + 3 + n, [colors.WHITE, F"{n+1})", item.inventoryFg, item.inventoryGlyph + "", colors.WHITE, item.name])
                else:
                    guiFunc.printFmt(self.console, posX + 30, posY + 3 + n, [colors.GRAY, F"{n+1})", item.inventoryFg, item.inventoryGlyph + "", colors.GRAY, item.name])
            else:
                if (n == self.itemIndex):
                    self.console.print(posX + 30, posY + 3 + n, F"{n+1})................", colors.WHITE)
                else:
                    self.console.print(posX + 30, posY + 3 + n, F"{n+1})................", colors.GRAY)
            n += 1

    def execute(self, game: Game, *args, **kwargs):
        inventory: Inventory
        _, (_, inventory) = self.world.get_components(Player, Inventory)[0]
        itemList = self.world.get_components(InventoryPosition, Item)

        self.handleInventoryInput(inventory, itemList)
        self.drawInventory(inventory, itemList)