import esper
from tcod import Console

import color
from gamestate import Game
from data import layout, lighting
from components import Position, Renderable, Player, FOV, Level

# (Level), (FOV), (Position, Renderable)
class EntityRenderSystem(esper.Processor):
    def __init__(self, console: Console) -> None:
        super().__init__()
        self.console = console
        self.world: esper.World = self.world

    def process(self, *args, **kwargs):
        pos: Position 
        rend: Renderable
        level: Level  
        playerFOV: FOV
        game: Game = kwargs["game"]
        _, level = self.world.get_component(Level)[0]
        _, (_, playerFOV) = self.world.get_components(Player, FOV)[0]    
        for _, (pos, rend) in sorted(self.world.get_components(Position, Renderable), key=lambda item: item[1][1].prio):
            if playerFOV.isVisible(pos.X, pos.Y) or (game.showMap):
                if game.useLighting:
                    hsl = color.toHLS(rend.fg)
                    hsl = (hsl[0], hsl[1] * (level.lightmap["level"][pos.X, pos.Y][0] / lighting.MAX_LIGHT_LEVEL), hsl[2])
                    rgb = color.toRGB(hsl)
                    rgb = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
                    self.console.print(layout.LEVEL_OFFSET_X + pos.X, layout.LEVEL_OFFSET_Y + pos.Y, rend.char, rgb, rend.bg)
                else:
                    self.console.print(layout.LEVEL_OFFSET_X + pos.X, layout.LEVEL_OFFSET_Y + pos.Y, rend.char, rend.fg, rend.bg)