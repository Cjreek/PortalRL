from tcod import Console
from tcod.context import Context

from game import Game
from systems.baseSystem import BaseSystem

class RenderFinalizeSystem(BaseSystem):
    def __init__(self, context: Context, console: Console) -> None:
        super().__init__()
        self.context = context
        self.console = console

    def execute(self, game: Game, *args, **kwargs):
        self.context.present(self.console)
        self.console.clear()