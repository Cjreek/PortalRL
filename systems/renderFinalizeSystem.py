from tcod import Console
from tcod.context import Context
import tcod

from game import Game
from data import layout
from systems.baseSystem import BaseSystem

class RenderFinalizeSystem(BaseSystem):
    def __init__(self, context: Context, console: Console, overlay: Console, windowConsole: Console) -> None:
        super().__init__()
        self.context = context
        self.console = console
        self.overlay = overlay
        self.windowConsole = windowConsole

    def execute(self, game: Game, *args, **kwargs):
        self.windowConsole.blit(self.console, 0, 0, 0, 0, self.console.width, self.console.height, 1, 1, [0,0,0])
        self.overlay.blit(self.console, layout.LEVEL_OFFSET_X, layout.LEVEL_OFFSET_Y, 0, 0, self.overlay.width, self.overlay.height, 0, 0.3, [0,0,0])
        self.context.present(self.console)
        self.console.clear()
        self.overlay.clear()
        self.windowConsole.clear(bg=[0,0,0])