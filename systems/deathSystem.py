from game import Game, GameState
from systems.baseSystem import BaseSystem
from components import Player, Position, Damageable, Velocity
from data import mobs

# (Player, Input, Velocity)
class DeathSystem(BaseSystem):   
    def execute(self, game: Game, *args, **kwargs):
        position: Position
        damageable: Damageable
        for entity, (position, damageable) in self.world.get_components(Position, Damageable):
            if damageable.isDead:
                if (self.world.has_component(entity, Player) and self.world.has_component(entity, Velocity)):
                    game.gameIsActive = False
                    game.changeState(GameState.GAME_OVER)
                if damageable.deadEntity:
                    mobs.spawn(self.world, damageable.deadEntity, position.X, position.Y)
                if damageable.removeOnDeath:
                    self.world.delete_entity(entity)