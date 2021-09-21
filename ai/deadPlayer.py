import esper

from rng import RNG
from game import Game, GameState
from ai import AIClass
from components import Input, Actor, Level

class DeadPlayerController(AIClass):
    def process(self, entity, actor: Actor, level: Level, game: Game, world: esper.World, rng: RNG) -> bool:
        input: Input = world.component_for_entity(entity, Input)
        if (input.Escape): 
            game.changeState(GameState.MAINMENU)
        return False