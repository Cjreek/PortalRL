import time
import esper
import tcod

from mainMenu import MainMenu

from game import Game, GameState
from data import layout

from systems import DebugSystem
from systems import LevelRenderSystem, EntityRenderSystem, GUIRenderSystem, RenderFinalizeSystem
from systems import InputSystem, LevelGenerationSystem, ComputeFOVSystem, ComputeLightingSystem, AISystem
from systems import MovementSystem, DeathSystem

class Engine:
    def __init__(self, title, screenWidth, screenHeight, tileset):
        self.context = tcod.context.new_terminal(screenWidth, screenHeight, 
            tileset=tcod.tileset.load_tilesheet(tileset, 16, 16, tcod.tileset.CHARMAP_CP437), 
            title=title,
            vsync=False)
        self.console = tcod.Console(screenWidth, screenHeight, order="F")
        # Game
        self.game = Game()
        self.game.registerStateChangeListener(self.gameStateChange)
        self.world: esper.World = None
        # Mainmenu
        self.mainMenu = MainMenu(self.game)
        # FPS
        self.frametimes = []
        self.lastFrame = 0

    def gameStateChange(self, newState):
        if newState == GameState.NEW_GAME:
            self.initECS()
            self.game.changeState(GameState.REQUEST_LEVEL)

    def calcFPS(self):
        self.frametimes.append(int(time.process_time()*1000) - self.lastFrame)
        self.lastFrame = int(time.process_time() * 1000)
        if sum(self.frametimes) >= 500:
            self.game.fps = 1000 / (sum(self.frametimes) / len(self.frametimes))
            self.frametimes = []
        
    def initECS(self):
        if self.world:
            self.world.clear_database()
            self.world.clear_cache()

        self.world = esper.World()
        
        self.world.add_processor(LevelGenerationSystem(), 5)
        self.world.add_processor(InputSystem(), 4)
        self.world.add_processor(DebugSystem(), 3)
        self.world.add_processor(AISystem(), 3)

        self.world.add_processor(MovementSystem(), 2)
        self.world.add_processor(DeathSystem(), 1)
        self.world.add_processor(ComputeFOVSystem(), 0)

        self.world.add_processor(ComputeLightingSystem(), -1)
        self.world.add_processor(LevelRenderSystem(self.console, layout.LEVEL_OFFSET_X, layout.LEVEL_OFFSET_Y), -2)
        self.world.add_processor(EntityRenderSystem(self.console), -3)
        self.world.add_processor(GUIRenderSystem(self.console), -4)
        self.world.add_processor(RenderFinalizeSystem(self.context, self.console), -99)

    def run(self):
        self.lastFrame = int(time.process_time() * 1000)
        while (True):
            if self.game.state == GameState.MAINMENU:
                self.mainMenu.handleEvents()
                self.mainMenu.render(self.context, self.console)
            else:
                self.world.process(game=self.game)
            self.calcFPS()
            time.sleep(0.001)