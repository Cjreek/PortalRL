import tcod.event

from game import Game, GameState
from systems.baseSystem import BaseSystem
from components import Debug, Input

# (Debug, Input)
class DebugSystem(BaseSystem):
    def execute(self, game: Game, *args, **kwargs):
        input: Input
        _, (_, input) = self.world.get_components(Debug, Input)[0]
        if (input.Debug):
            if input.RawKey == tcod.event.K_F2:
                game.useLighting = not game.useLighting
            if input.RawKey == tcod.event.K_F3:
                game.showMap = not game.showMap
            if input.RawKey == tcod.event.K_F4:
                game.showFOV = not game.showFOV
            if input.RawKey == tcod.event.K_F5:
                game.changeState(GameState.REQUEST_LEVEL)