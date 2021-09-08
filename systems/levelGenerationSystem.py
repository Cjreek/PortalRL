import random
import esper

from gamestate import Game, GameState
from components import Player, Position, Level, Debug, Input
from data import mobs, layout

import generation

# (Level), (Player, Position)
class LevelGenerationSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
        self.world: esper.World = self.world

    def process(self, *args, **kwargs):
        game: Game = kwargs["game"]
        if (game.state == GameState.REQUEST_LEVEL):
            self.world.clear_database()

            seed = int.from_bytes(random.randbytes(4), byteorder='little', signed=False)
            level = Level(layout.LEVEL_WIDTH, layout.LEVEL_HEIGHT, seed)
            self.world.create_entity(level)
            
            player = mobs.spawn(self.world, mobs.PLAYER, 0, 0)
            self.world.create_entity(Debug(), Input())

            playerPos = self.world.component_for_entity(player, Position)
            generation.generateLevel(self.world, level, playerPos, 5, 10, 10, 20)

            game.state = GameState.PLAYING