import os
import pygame.display

from engine import Engine
from data import layout

def disablePyGame():
    pygame.display.init()
    pygame.display.quit()

def main():
    disablePyGame()
    engine = Engine("PortalRL", layout.SCREEN_WIDTH, layout.SCREEN_HEIGHT, os.path.join("resources", "tilesets", "Cooz-curses-square-16x16.png"))
    engine.run()
    
if __name__ == "__main__":
    main()