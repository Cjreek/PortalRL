import random

from game import Game, GameState
from systems.baseSystem import BaseSystem
from components import Position, Level, Debug, Input
from data import mobs, layout

import generation

# (Level), (Player, Position)
class LevelGenerationSystem(BaseSystem):
    def canExecute(self, gameState: GameState):
        return gameState in [GameState.REQUEST_LEVEL]

    def execute(self, game: Game, *args, **kwargs):
        self.world.clear_database()
        self.world.clear_cache()

        seed = random.getrandbits(32)
        level = Level(layout.LEVEL_WIDTH, layout.LEVEL_HEIGHT, seed)
        self.world.create_entity(level)
        
        player = mobs.spawn(self.world, mobs.PLAYER, 0, 0)
        self.world.create_entity(Debug(), Input())

        playerPos = self.world.component_for_entity(player, Position)
        generation.generateLevel(self.world, level, playerPos, 5, 10, 10, 20)

        game.changeState(GameState.PLAYING)