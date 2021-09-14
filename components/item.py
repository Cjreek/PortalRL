from typing import Tuple

from data import colors

class Item:
    def __init__(self, name: str, invGlyph: str, invFg: Tuple[int, int, int], invBg: Tuple[int, int, int] = colors.BLACK) -> None:
        self.name = name
        self.inventoryGlyph = invGlyph
        self.inventoryFg = invFg
        self.inventoryBg = invBg