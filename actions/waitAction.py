
import esper

from game import Game
from actions.action import Action

class WaitAction(Action):
    def __init__(self, costModifier: int = 0) -> None:
        super().__init__(costModifier)
    
    def getPointCost(self) -> int:
        return 0

    def perform(self, game: Game, world: esper.World, entity):
        pass