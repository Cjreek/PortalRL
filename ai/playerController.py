from random import Random
import esper

from game import Game, GameState
from ai import AIClass
from components import Input, Velocity

class PlayerController(AIClass):
    def process(self, entity, game: Game, world: esper.World, rng: Random):
        input: Input = world.component_for_entity(entity, Input)
        velocity: Velocity = world.component_for_entity(entity, Velocity)

        result = True
        if (input.Up): velocity.addStep(0, -1)
        elif (input.Down): velocity.addStep(0, 1)
        elif (input.Left): velocity.addStep(-1, 0)
        elif (input.Right): velocity.addStep(1, 0)
        elif (input.UpLeft): velocity.addStep(-1, -1)
        elif (input.UpRight): velocity.addStep(1, -1)
        elif (input.DownLeft): velocity.addStep(-1, 1)
        elif (input.DownRight): velocity.addStep(1, 1)
        elif (input.Wait): pass
        else:
            result = False
            if (input.Escape): game.changeState(GameState.MAINMENU)

        input.clear()

        return result