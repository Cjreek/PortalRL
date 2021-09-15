from typing import List
from enum import Enum, auto

class GameState(Enum):
    MAINMENU = auto(),
    NEW_GAME = auto(),
    REQUEST_LEVEL = auto(),
    PLAYING = auto()
    INVENTORY = auto()
    GAME_OVER = auto()

class Game:
    def __init__(self) -> None:
        self.__state = GameState.MAINMENU
        self.gameIsActive = False
        self.fps = 0
        self.stateListeners = []
        self.log: List[str] = []
        # Debug Flags
        self.useLighting = True
        self.showMap = False
        self.showFOV = False

    @property
    def state(self):
        return self.__state

    def reset(self):
        self.log.clear()
        self.stateListeners.clear

    def changeState(self, state: GameState):
        if (self.__state != state):
            self.__state = state
            for listener in self.stateListeners:
                listener(self.__state)

    def registerStateChangeListener(self, listener):
        if not listener in self.stateListeners:
            self.stateListeners.append(listener)

    def logMessage(self, message: str):
        self.log.append(message)
