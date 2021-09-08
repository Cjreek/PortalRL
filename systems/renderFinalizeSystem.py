import esper
from tcod import Console
from tcod.context import Context

class RenderFinalizeSystem(esper.Processor):
    def __init__(self, context: Context, console: Console) -> None:
        super().__init__()
        self.context = context
        self.console = console

    def process(self, *args, **kwargs):
        self.context.present(self.console)
        self.console.clear()