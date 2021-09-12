from tcod import Console

import guiFunc

from game import Game, GameState
from components import Player, Inventory, InventoryPosition, Info, Item
from systems.baseSystem import BaseSystem
from data import layout

class InventoryRenderSystem(BaseSystem):
    def __init__(self, console: Console) -> None:
        super().__init__()
        self.console = console

    def canExecute(self, gameState: GameState):
        return gameState in [GameState.INVENTORY]

    def drawInventory(self):
        self.console.clear(bg=[0,0,0])
        posX = layout.LEVEL_OFFSET_X + (layout.LEVEL_WIDTH // 2) - (layout.INVENTORY_WIDTH // 2)
        posY = layout.LEVEL_OFFSET_Y +(layout.LEVEL_HEIGHT // 2) - (layout.INVENTORY_HEIGHT // 2)

        guiFunc.drawFrame(self.console, posX, posY, posX + layout.INVENTORY_WIDTH, posY + layout.INVENTORY_HEIGHT, text="Inventory")

        n = 0
        inventory: Inventory
        _, (_, inventory) = self.world.get_components(Player, Inventory)[0]

        info: Info
        item: Item
        for _, (_, info, item)  in self.world.get_components(InventoryPosition, Info, Item):
            self.console.print(posX + 30, posY + 3 + n, chr(ord("a") + n) + ") " +  info.name)
            n += 1

    def execute(self, game: Game, *args, **kwargs):
        self.drawInventory()