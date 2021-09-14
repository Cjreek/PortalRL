from typing import List
from tcod import Console
import tcod

import guiFunc

from game import Game, GameState
from components import Player, Inventory, InventoryPosition, Info, Item, Input
from systems.baseSystem import BaseSystem
from data import layout, colors

class InventoryRenderSystem(BaseSystem):
    def __init__(self, console: Console) -> None:
        super().__init__()
        self.console = console
        # control
        self.itemIndex = 0

    def canExecute(self, gameState: GameState):
        return gameState in [GameState.INVENTORY]

    def handleInventoryInput(self, itemList: List):
        input: Input
        _, (_, input) = self.world.get_components(Player, Input)[0]
        if (input.Up):
            self.itemIndex = max(self.itemIndex - 1, 0)
        elif (input.Down):
            self.itemIndex = min(self.itemIndex + 1, len(itemList) - 1)
        elif (input.RawKey >= tcod.event.K_a) and (input.RawKey <= tcod.event.K_z): # TODO: I-Key is reserved for opening/closing inventory
            calcIndex = input.RawKey - tcod.event.K_a
            if (calcIndex < len(itemList)):
                self.itemIndex = calcIndex

    def drawInventory(self, itemList: List):
        posX = layout.LEVEL_OFFSET_X + (layout.LEVEL_WIDTH // 2) - (layout.INVENTORY_WIDTH // 2)
        posY = layout.LEVEL_OFFSET_Y +(layout.LEVEL_HEIGHT // 2) - (layout.INVENTORY_HEIGHT // 2)

        guiFunc.drawFrame(self.console, posX, posY, posX + layout.INVENTORY_WIDTH, posY + layout.INVENTORY_HEIGHT, text="Inventory")

        n = 0
        inventory: Inventory
        _, (_, inventory) = self.world.get_components(Player, Inventory)[0]

        item: Item
        for _, (_, item) in itemList:
            if (n == self.itemIndex):
                guiFunc.printFmt(self.console, posX + 30, posY + 3 + n, [item.inventoryFg, item.inventoryGlyph + " ", colors.WHITE, item.name])
            else:
                guiFunc.printFmt(self.console, posX + 30, posY + 3 + n, [item.inventoryFg, item.inventoryGlyph + " ", colors.GRAY, item.name])
            n += 1

    def execute(self, game: Game, *args, **kwargs):
        itemList = self.world.get_components(InventoryPosition, Item)
        self.handleInventoryInput(itemList)
        self.drawInventory(itemList)