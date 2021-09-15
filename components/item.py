from __future__ import annotations

from typing import Tuple

from data import colors
from data.enums import EquipmentSlot

class Item:
    def __init__(self, name: str, invGlyph: str, equipmentSlot: EquipmentSlot, invFg: Tuple[int, int, int] = colors.ITEM, invBg: Tuple[int, int, int] = colors.BLACK) -> None:
        self.name = name
        self.equipmentSlot = equipmentSlot
        self.inventoryGlyph = invGlyph
        self.inventoryFg = invFg
        self.inventoryBg = invBg