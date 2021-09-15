from typing import Tuple, Optional, Dict

from components.item import Item
from data.enums import EquipmentSlot

class Equipment:
    __emptyItem = (None, None)

    def __init__(self) -> None:
        self.items: Dict[EquipmentSlot, Tuple[int, Item]] = {}

    def getItem(self, slot) -> Optional[Tuple[int, Item]]:
        return self.items.get(slot, Equipment.__emptyItem)

    def equip(self, item: Tuple[int, Item]) -> Optional[Tuple[int, Item]]:
        _, itemComp = item
        if itemComp.equipmentSlot != EquipmentSlot.NONE:
            oldItem = self.items.get(itemComp.equipmentSlot, Equipment.__emptyItem)
            self.items[itemComp.equipmentSlot] = item
            return oldItem
        else:
            return item

    def unequip(self, slot: EquipmentSlot) -> Optional[Tuple[int, Item]]:
        oldItem = self.items.get(slot, Equipment.__emptyItem)
        self.items[slot] = Equipment.__emptyItem
        return oldItem