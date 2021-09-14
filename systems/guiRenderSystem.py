from math import dist
from tcod import Console

import guiFunc

from game import Game
from systems.baseSystem import BaseSystem
from components import Position, Renderable, FOV
from components import Player, Info, Damageable, Velocity, Blocking
from data import layout, colors

# (Position, Renderable)
class GUIRenderSystem(BaseSystem):
    def __init__(self, console: Console) -> None:
        super().__init__()
        self.console = console

    def execute(self, game: Game, *args, **kwargs):
        guiFunc.drawFrame(self.console, layout.LBAR_OFFSET_X, layout.LBAR_OFFSET_Y, layout.LBAR_OFFSET_X + layout.LBAR_WIDTH, layout.LBAR_OFFSET_Y + layout.LBAR_HEIGHT)
        guiFunc.drawFrame(self.console, layout.RBAR_OFFSET_X, layout.RBAR_OFFSET_Y, layout.RBAR_OFFSET_X + layout.RBAR_WIDTH, layout.RBAR_OFFSET_Y + layout.RBAR_HEIGHT)
        guiFunc.drawFrame(self.console, layout.BBAR_OFFSET_X, layout.BBAR_OFFSET_Y, layout.BBAR_OFFSET_X + layout.BBAR_WIDTH, layout.BBAR_OFFSET_Y + layout.BBAR_HEIGHT)
        
        # Player HP
        info: Info
        playerHP: Damageable
        playerFov: FOV
        playerPos: Position
        playerEntity, (_, playerPos, info, playerHP, playerFov) = self.world.get_components(Player, Position, Info, Damageable, FOV)[0]
        self.console.print(1, 4, info.name)
        guiFunc.drawBar(self.console, 1, 5, layout.LBAR_WIDTH-2, 0, playerHP.maxHP, playerHP.hp, [0,0,0], [255, 0, 0])
        self.console.print(1, 5, "HP: " + str(playerHP.hp) + "/" + str(playerHP.maxHP))

        # Mob List
        mobHP: Damageable
        position: Position
        n = 0
        mobList = self.world.get_components(Velocity, Position, Info, Damageable)
        mobList.sort(key=lambda item: dist([playerPos.X, playerPos.Y], [item[1][1].X, item[1][1].Y]))
        for mobEntity, (_, position, info, mobHP) in mobList:
            if playerFov.isVisible(position.X, position.Y) and (mobEntity != playerEntity):
                if dist([playerPos.X, playerPos.Y], [position.X, position.Y]) < 2:
                    self.console.print(1, 8+n*2, info.name, fg=[255,255,0])
                else:
                    self.console.print(1, 8+n*2, info.name)            
                guiFunc.drawBar(self.console, 1, 9+n*2, layout.LBAR_WIDTH-2, 0, mobHP.maxHP, mobHP.hp, [0,0,0], [255, 0, 0])
                n += 1

        # Message Log
        n = 1
        for msg in reversed(game.log):
            if n > layout.BBAR_HEIGHT - 2:
                break
            self.console.print(20, layout.BBAR_OFFSET_Y + n, msg, colors.WHITE)
            n += 1

        ## DEBUG ##
        entityCount = len(self.world.get_components(Blocking, Position, Renderable))
        self.console.print(1, 1, "FPS:" + str(int(game.fps)))
        self.console.print(1, 2, "Entities: " + str(entityCount))
        # console.print(1, layout.BBAR_OFFSET_Y+1, "Seed: " + str(self.level.seed))
        ##########