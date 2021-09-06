import pygame
import pygame.mixer

import layout
import engine

def main():
    pygame.display.init()
    pygame.display.quit()
    pygame.mixer.init()

    engine = engine.Engine("Cjreek's Roguelike", layout.SCREEN_WIDTH, layout.SCREEN_HEIGHT, "data\Cooz-curses-square-16x16.png")
    engine.run()
        
if __name__ == "__main__":
    main()