from typing import Optional, Dict

from data.enums import EquipmentSlot
from data.types import InventoryItem

class Equipment:
    def __init__(self) -> None:
        self.items: Dict[EquipmentSlot, InventoryItem] = {}

    def getItem(self, slot) -> Optional[InventoryItem]:
        return self.items.get(slot)

    def equip(self, item: InventoryItem) -> Optional[InventoryItem]:
        if item.itemData.equipmentSlot != EquipmentSlot.NONE:
            oldItem = self.items.get(item.itemData.equipmentSlot)
            self.items[item.itemData.equipmentSlot] = item
            return oldItem
        else:
            return item

    def unequip(self, slot: EquipmentSlot) -> Optional[InventoryItem]:
        oldItem = self.items.get(slot)
        self.items[slot] = None
        return oldItem