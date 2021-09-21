import esper

from game import Game, GameState
from components.level import Level
class BaseSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
        self.world: esper.World = self.world

    def reset(self):
        pass

    def canExecute(self, gameState: GameState):
        return gameState in [GameState.PLAYING, GameState.INVENTORY, GameState.GAME_OVER]

    def execute(self, game: Game, level: Level):
        pass

    def process(self, *args, **kwargs):
        game: Game = kwargs["game"]
        _, level = next(iter(self.world.get_component(Level) or []), (None, None))
        
        # _, level = levelList[0] if len(levelList) > 0 else None, None            
        if game.state == GameState.REQUEST_LEVEL:
            self.reset()
        if self.canExecute(game.state):
            self.execute(game, level)