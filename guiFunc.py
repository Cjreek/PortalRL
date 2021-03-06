from typing import Tuple, List
from collections.abc import Iterable

from tcod import Console
import tcod

from data import colors

def drawFrame(console: Console, x1: int, y1: int, x2: int, y2: int, text: str = ""):
    console.default_fg = [255,255,255]
    console.default_bg = colors.GUI_BACKGROUND
    console.print_frame(x1, y1, x2-x1, y2-y1, text, True, tcod.BKGND_SET)

def drawBar(console: Console, x: int, y: int, width: int, min: int, max: int, value: int, bg: Tuple[int, int, int], fill: Tuple[int, int, int]):
    console.draw_rect(x, y, width, 1, ord(" "), bg=bg)
    if (value > min):
        console.draw_rect(x, y, int(width * (value / (max-min))), 1, ord(" "), bg=fill)

def printFmt(console: Console, x: int, y: int, format: List):
    currentColor = console.default_fg
    currPos = x
    for item in format:
        if isinstance(item, str):
            console.print(currPos, y, item, currentColor)
            currPos += len(item)
        elif isinstance(item, Iterable) and (len(item) == 3):
            currentColor = item
