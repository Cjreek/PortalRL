from typing import Optional, List

from tcod import Console
from tcod.context import Context
import tcod.event
import tcod.constants

from game import Game, GameState

class MenuItem:
    def __init__(self, title: str, visibleFunc, executeFunc, hotkey) -> None:
        self.title = title
        self.visibleFunc = visibleFunc
        self.executeFunc = executeFunc
        self.hotkey = hotkey

class MainMenu(tcod.event.EventDispatch[bool]):
    def __init__(self, game: Game) -> None:
        self.game = game
        self.menuItems = [
            MenuItem("(R)esume Game", lambda: game.gameIsActive, self.resumeGame, tcod.event.K_r), 
            MenuItem("(N)ew Game", lambda: True, self.newGame, tcod.event.K_n), 
            MenuItem("(Q)uit", lambda: True, self.quitGame, tcod.event.K_q)
        ]
        self.maxItemWidth = max((len(item.title) for item in self.menuItems))
        self.visibleItems: List[MenuItem] = []
        self.selectedIndex = 0
        self.game.registerStateChangeListener(self.gameStateChange)

    def gameStateChange(self, newState: GameState):
        if newState == GameState.MAINMENU:
            self.selectedIndex = 0

    def quitGame(self):
        raise SystemExit()

    def newGame(self):
        self.game.gameIsActive = True
        self.game.changeState(GameState.NEW_GAME)

    def resumeGame(self):
        self.game.changeState(GameState.PLAYING)

    def ev_quit(self, event: tcod.event.Quit) -> Optional[bool]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[bool]:
        key = event.sym

        hotkeyItem = next((item for item in self.menuItems if item.hotkey == key), None)
        if (hotkeyItem):
            hotkeyItem.executeFunc()
        elif key in (tcod.event.K_UP, tcod.event.K_KP_8, tcod.event.K_k):
            self.selectedIndex = max(self.selectedIndex - 1, 0) 
        elif key in (tcod.event.K_DOWN, tcod.event.K_KP_2, tcod.event.K_j):
           self.selectedIndex = min(self.selectedIndex + 1, len(self.visibleItems)-1)
        elif (key == tcod.event.K_ESCAPE) and (self.game.gameIsActive):
            self.resumeGame()
        elif key == tcod.event.K_RETURN:
            self.visibleItems[self.selectedIndex].executeFunc()

    def handleEvents(self):
        for event in tcod.event.get():
            self.dispatch(event)

    def render(self, context: Context, console: Console):
        if self.game.state == GameState.MAINMENU:
            centerX = console.width // 2 - (self.maxItemWidth // 2)
            n = 0
            self.visibleItems.clear()
            for i in range(len(self.menuItems)):
                if self.menuItems[i].visibleFunc():
                    self.visibleItems.append(self.menuItems[i])
                    if n == self.selectedIndex:
                        console.print(centerX, 25 + n*2, self.menuItems[i].title, [255, 255, 255], alignment=tcod.constants.LEFT)
                    else:
                        console.print(centerX, 25 + n*2, self.menuItems[i].title, [160, 160, 160], alignment=tcod.constants.LEFT)
                    n += 1
            context.present(console)
            console.clear(bg=[0,0,0])