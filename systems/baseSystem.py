import esper

from game import Game, GameState

class BaseSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
        self.world: esper.World = self.world

    def reset(self):
        pass

    def canExecute(self, gameState: GameState):
        return gameState in [GameState.PLAYING, GameState.GAME_OVER]

    def execute(self, game: Game, *args, **kwargs):
        pass

    def process(self, *args, **kwargs):
        game: Game = kwargs["game"]
        del kwargs["game"]
        if game.state == GameState.REQUEST_LEVEL:
            self.reset()
        if self.canExecute(game.state):
            self.execute(game, *args, **kwargs)