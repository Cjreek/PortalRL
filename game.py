import esper
from enum import Enum, auto

class GameState(Enum):
    MAINMENU = auto(),
    NEW_GAME = auto(),
    REQUEST_LEVEL = auto(),
    PLAYING = auto()
    GAME_OVER = auto()

class Game:
    def __init__(self) -> None:
        self.__state = GameState.MAINMENU
        self.useLighting = True
        self.showMap = False
        self.gameIsActive = False
        self.fps = 0
        self.stateListeners = []

    @property
    def state(self):
        return self.__state

    def changeState(self, state: GameState):
        if (self.__state != state):
            self.__state = state
            for listener in self.stateListeners:
                listener(self.__state)

    def registerStateChangeListener(self, listener):
        if not listener in self.stateListeners:
            self.stateListeners.append(listener)
