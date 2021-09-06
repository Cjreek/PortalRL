from __future__ import annotations
from typing import TYPE_CHECKING

from collections import deque
from enum import IntEnum

from tcod import Console
import tcod.event

if TYPE_CHECKING:
    from actions import Action

class GameStateEnum(IntEnum):
    MAINMENU = 0,
    GAME = 1

class GameState(tcod.event.EventDispatch[Action]):
    def __init__(self, engine) -> None:
        super().__init__()
        self.actionQueue = deque([], 1)
        self.engine = engine

    def queueAction(self, action: Action):
        self.actionQueue.append(action)

    def hasAction(self):
        return len(self.actionQueue) > 0

    def getAction(self):
        return self.actionQueue.popleft()

    def enter(self):
        pass

    def tick(self):
        pass

    def render(self, console: Console):
        pass