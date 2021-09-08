from typing import Tuple

from tcod import Console
import tcod

def drawFrame(console: Console, x1: int, y1: int, x2: int, y2: int):
    console.default_bg = [64,64,64]
    console.print_frame(x1, y1, x2-x1, y2-y1, "", True, tcod.BKGND_SET)
    pass

def drawBar(console: Console, x: int, y: int, width: int, min: int, max: int, value: int, bg: Tuple[int, int, int], fill: Tuple[int, int, int]):
    console.draw_rect(x, y, width, 1, ord(" "), bg=bg)
    if (value > min):
        console.draw_rect(x, y, int(width * (value / (max-min))), 1, ord(" "), bg=fill)