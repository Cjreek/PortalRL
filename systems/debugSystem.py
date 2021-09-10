import esper
import tcod.event

from gamestate import Game, GameState
from components import Debug, Input

# (Player, Input, Velocity)
class DebugSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
        self.world: esper.World = self.world

    def process(self, *args, **kwargs):
        game: Game = kwargs["game"]
        input: Input
        _, (_, input) = self.world.get_components(Debug, Input)[0]
        if (input.Debug):
            if input.DebugKey == tcod.event.K_F2:
                game.useLighting = not game.useLighting
            if input.DebugKey == tcod.event.K_F3:
                game.showMap = not game.showMap
            if input.DebugKey == tcod.event.K_F5:
                game.state = GameState.REQUEST_LEVEL