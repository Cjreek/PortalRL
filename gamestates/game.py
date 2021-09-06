from __future__ import annotations
from typing import TYPE_CHECKING

from tcod import Console

if TYPE_CHECKING:
    import factions
    import renderprio
    import generation
    from gamestates.gamestate import GameState
    from entity import Entity
    from components.damageable import Living
    from components.lightsource import LightSource
    from components.player import Player

class Game(GameState):

    def __init__(self, engine) -> None:
        super().__init__(engine)
        self.player: Entity = None

    def enter(self):
        self.player = Entity("Player", "☻", [255,0,0], [Player(10, 2), Living(10), LightSource((255,255,0), False, 8)], factions.PLAYER, renderPrio=renderprio.HIGH)
        debugSeed=2839612019 #2921916982 # int.from_bytes(random.randbytes(4), 'little', signed=False)
        self.level = generation.generateLevel(5, 10, 10, 20, self.engine, self, seed=debugSeed)

    def tick(self):
        self.level.tick()

    def render(self, console: Console):
        self.level.render(console)
        pass