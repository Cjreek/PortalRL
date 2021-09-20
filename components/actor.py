from typing import Deque
from collections import deque
from actions.action import Action

class Actor:
    def __init__(self, initiative: int, actionPoints: int, startingInitiative: int = None) -> None:
        self.maxInitiative = initiative
        if startingInitiative is not None:
            self.initiative = startingInitiative
        else:
            self.initiative = self.maxInitiative
        self.maxActionPoints = actionPoints
        self.actionPoints = actionPoints
        self.actionQueue: Deque[Action] = deque([])
        self.currentAction: Action = None

    def tickInitiative(self):
        if self.initiative > 0:
            self.initiative -= 1

    def resetInitiative(self):
        self.initiative = self.maxInitiative

    def resetActionPoints(self):
        self.actionPoints = self.maxActionPoints

    @property
    def isReady(self) -> bool:
        return self.initiative <= 0

    def queueAction(self, action: Action):
        if not self.currentAction:
            self.currentAction = action
        else:
            self.actionQueue.append(action)

    def nextAction(self) -> bool:
        if len(self.actionQueue) > 0:
            self.currentAction = self.actionQueue.popleft()
            return True
        else:
            self.currentAction = None
            return False