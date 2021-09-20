import esper

from rng import RNG
from game import Game, GameState
from ai import AIClass
from components import Input, Actor

class DeadPlayerController(AIClass):
    def process(self, entity, actor: Actor, game: Game, world: esper.World, rng: RNG) -> bool:
        input: Input = world.component_for_entity(entity, Input)
        if (input.Escape): 
            game.changeState(GameState.MAINMENU)
        return False