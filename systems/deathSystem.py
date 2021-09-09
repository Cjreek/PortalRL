import esper

from gamestate import Game, GameState
from components import Player, Position, Damageable
from data import mobs

# (Player, Input, Velocity)
class DeathSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
        self.world: esper.World = self.world
    
    def process(self, *args, **kwargs):
        game: Game = kwargs["game"]
        position: Position
        damageable: Damageable
        for entity, (position, damageable) in self.world.get_components(Position, Damageable):
            if damageable.isDead:
                if (self.world.has_component(entity, Player)):
                    game.state = GameState.GAME_OVER
                if damageable.deadEntity:
                    mobs.spawn(self.world, damageable.deadEntity, position.X, position.Y)
                if damageable.removeOnDeath:
                    self.world.delete_entity(entity)