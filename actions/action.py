import esper

from game import Game

class Action:
    def __init__(self, costModifier: int = 0) -> None:
        self.totalCost = self.getPointCost() + costModifier
        self.remainingCost = self.totalCost

    def getPointCost(self) -> int:
        return 1
    
    def perform(self, game: Game, world: esper.World, entity):
        pass