from typing import Tuple
from data import renderprio

class Renderable:
    def __init__(self, char: str, fg: Tuple[int, int, int], bg: Tuple[int, int, int] = (0,0,0), prio: int = renderprio.NORMAL) -> None:
        self.char = char
        self.fg = fg
        self.bg = bg
        self.prio = prio