from enum import Enum, auto

class GameState(Enum):
    MAINMENU = auto(),
    REQUEST_LEVEL = auto(),
    PLAYING = auto()
    GAME_OVER = auto()

class Game:
    def __init__(self) -> None:
        self.state = GameState.REQUEST_LEVEL
        self.useLighting = True
        self.showMap = False
        self.fps = 0