import tcod
from tcod import Console

from game import Game
from systems.baseSystem import BaseSystem
from components import Player, FOV, Input

class OverlayRenderSystem(BaseSystem):
    def __init__(self, overlay: Console) -> None:
        super().__init__()
        self.overlay = overlay

    def execute(self, game: Game, *args, **kwargs):
        if game.showFOV:
            playerFov: FOV
            _, (_, playerFov) = self.world.get_components(Player, FOV)[0]
            self.overlay.rgba[playerFov.fov] = ord(' '), [0, 0, 0, 0], [255, 0, 0, 255]
        
        # Mouse cursor
        input: Input
        _, (_, input) = self.world.get_components(Player, Input)[0]
        if (input.MouseLevelX >= 0) and (input.MouseLevelX < self.overlay.width) and (input.MouseLevelY >= 0) and (input.MouseLevelY < self.overlay.height):
            self.overlay.rgb[input.MouseLevelX, input.MouseLevelY] = ord(' '), tcod.white, tcod.white