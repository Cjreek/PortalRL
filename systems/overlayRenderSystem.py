from tcod import Console

from game import Game
from systems.baseSystem import BaseSystem
from components import Player, FOV

class OverlayRenderSystem(BaseSystem):
    def __init__(self, overlay: Console) -> None:
        super().__init__()
        self.overlay = overlay

    def execute(self, game: Game, *args, **kwargs):
        if game.showFOV:
            playerFov: FOV
            _, (_, playerFov) = self.world.get_components(Player, FOV)[0]
            self.overlay.rgba[playerFov.fov] = ord(' '), [0, 0, 0, 0], [255, 0, 0, 255]