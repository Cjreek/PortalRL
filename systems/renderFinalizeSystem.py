from tcod import Console
from tcod.context import Context

from game import Game
from data import layout
from systems.baseSystem import BaseSystem

class RenderFinalizeSystem(BaseSystem):
    def __init__(self, context: Context, console: Console, overlay: Console) -> None:
        super().__init__()
        self.context = context
        self.console = console
        self.overlay = overlay

    def execute(self, game: Game, *args, **kwargs):
        if game.showFOV:
            self.overlay.blit(self.console, layout.LEVEL_OFFSET_X, layout.LEVEL_OFFSET_Y, 0, 0, self.overlay.width, self.overlay.height, 0, 0.2, [0,0,0])
        self.context.present(self.console)
        self.console.clear()
        self.overlay.clear()