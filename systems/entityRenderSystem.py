from tcod import Console

import colorFunc

from game import Game
from systems.baseSystem import BaseSystem
from components import Position, Renderable, Player, FOV, Level
from data import layout, lighting

# (FOV), (Position, Renderable)
class EntityRenderSystem(BaseSystem):
    def __init__(self, console: Console) -> None:
        super().__init__()
        self.console = console

    def execute(self, game: Game, level: Level):
        pos: Position 
        rend: Renderable
        playerFOV: FOV
        _, (_, playerFOV) = self.world.get_components(Player, FOV)[0]    
        for _, (pos, rend) in sorted(self.world.get_components(Position, Renderable), key=lambda item: item[1][1].prio):
            if playerFOV.isVisible(pos.X, pos.Y) or (game.showMap):
                if game.useLighting:
                    hsl = colorFunc.toHLS(rend.fg)
                    hsl = (hsl[0], hsl[1] * (level.lightmap["level"][pos.X, pos.Y] / lighting.MAX_LIGHT_LEVEL), hsl[2])
                    rgb = colorFunc.toRGB(hsl)
                    rgb = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
                    self.console.print(layout.LEVEL_OFFSET_X + pos.X, layout.LEVEL_OFFSET_Y + pos.Y, rend.char, rgb, rend.bg)
                else:
                    self.console.print(layout.LEVEL_OFFSET_X + pos.X, layout.LEVEL_OFFSET_Y + pos.Y, rend.char, rend.fg, rend.bg)