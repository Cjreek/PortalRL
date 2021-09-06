from __future__ import annotations
from typing import TYPE_CHECKING

import time
import math

import tcod

import imports
if TYPE_CHECKING:
    import layout
    import gui
    from gamestates.gamestate import GameState, GameStateEnum
    from gamestates.game import Game
    from gamestates.mainmenu import MainMenuState
    # from events import EventHandler
    # from entity import Entity
    from components.damageable import Damageable, Living

class Engine:
    def __init__(self, title, screenWidth, screenHeight, tileset):
        self.context = tcod.context.new_terminal(screenWidth, screenHeight, 
            tileset=tcod.tileset.load_tilesheet(tileset, 16, 16, tcod.tileset.CHARMAP_CP437), 
            title=title,
            vsync=False)

        self.console = tcod.Console(screenWidth, screenHeight, order="F")
        # self.eventHandler = EventHandler(self)
        self.gameStates = [MainMenuState(self), Game(self)]
        self.state = GameStateEnum.MAINMENU
        self.setState(GameStateEnum.GAME)
        

        # self.player: Entity = Entity("Player", "☻", [255,0,0], [Player(10, 2), Living(10), LightSource((255,255,0), False, 8)], factions.PLAYER, renderPrio=renderprio.HIGH)

        # debugSeed=2839612019 #2921916982 # int.from_bytes(random.randbytes(4), 'little', signed=False)
        # self.level = generateLevel(5, 10, 10, 20, self, seed=debugSeed)

        self.lastFrame = int(time.process_time()*1000)
        self.lastFPS = 0
        self.frametimes = []
        # self.actionQueue: deque = deque([], 1)
        self.useLighting = True

    @property
    def currentState(self) -> GameState:
        return self.gameStates[self.state]

    def setState(self, state: GameStateEnum):
        self.state = state
        self.currentState.enter()

    def handleEvents(self):
        for event in tcod.event.get():
            action = self.eventHandler.dispatch(event)
            if not (action is None):
                self.currentState.queueAction(action)
    
    def renderGUI(self, console: tcod.Console):
        gui.drawFrame(console, layout.LBAR_OFFSET_X, layout.LBAR_OFFSET_Y, layout.LBAR_OFFSET_X + layout.LBAR_WIDTH, layout.LBAR_OFFSET_Y + layout.LBAR_HEIGHT)
        gui.drawFrame(console, layout.BBAR_OFFSET_X, layout.BBAR_OFFSET_Y, layout.BBAR_OFFSET_X + layout.BBAR_WIDTH, layout.BBAR_OFFSET_Y + layout.BBAR_HEIGHT)
        
        playerHP: Damageable = self.player.getComponent(Living)
        if playerHP:
            console.print(1, 4, "Player")
            gui.drawBar(console, 1, 5, layout.LBAR_WIDTH-2, 0, playerHP.maxHP, playerHP.hp, [0,0,0], [255, 0, 0])
            console.print(1, 5, "HP: " + str(playerHP.hp) + "/" + str(playerHP.maxHP))

        n = 0
        self.level.entities.sort(key=lambda entity: math.dist([self.player.x, self.player.y], [entity.x, entity.y]))
        for i in range(len(self.level.entities)):
            entity: entity.Entity = self.level.entities[i]
            if self.level.isVisible(entity.x, entity.y) and (entity != self.player):
                entityHP: Damageable = entity.getComponent(Living)
                if (entityHP):
                    if math.dist([self.player.x, self.player.y], [entity.x, entity.y]) < 2:
                        console.print(1, 7+n*2, entity.name, fg=[255,255,0])
                    else:
                        console.print(1, 7+n*2, entity.name)
                    
                    gui.drawBar(console, 1, 8+n*2, layout.LBAR_WIDTH-2, 0, entityHP.maxHP, entityHP.hp, [0,0,0], [255, 0, 0])
                    n += 1


        ## DEBUG ##
        if sum(self.frametimes) >= 500:
            self.lastFPS = 1000 / (sum(self.frametimes) / len(self.frametimes))
            self.frametimes = []
        console.print(1, 1, "FPS:" + str(int(self.lastFPS)))
        console.print(1, 2, "Entities: " + str(len(self.level.entities)))
        console.print(1, layout.BBAR_OFFSET_Y+1, "Seed: " + str(self.level.seed))
        ##########

    def render(self):
        self.currentState.render(self.console)
        # self.level.render(self.console)
        # self.renderGUI(self.console)
        self.context.present(self.console)

        self.frametimes.append(int(time.process_time()*1000) - self.lastFrame)
        self.lastFrame = int(time.process_time() * 1000)
        self.console.clear(bg=[0,0,0])

    def run(self):
        # TICKS_PER_SECOND = 30
        # MS_PER_TICK = 1000 / TICKS_PER_SECOND

        # lastTick = int(time.process_time() * 1000)
        while (True):
            self.handleEvents()
            self.currentState.tick()
            self.render()
            
            # if ((int(time.process_time() * 1000) - lastTick) >= MS_PER_TICK):
                # lastTick = int(time.process_time() * 1000)
            # TODO: Performance. Sleep(0) klappt nicht
            