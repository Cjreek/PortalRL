from typing import List
from data.types import InventoryItem

class Inventory:
    def __init__(self, maxCapacity: int) -> None:
        self.maxCapacity = maxCapacity
        self.items: List[InventoryItem] = []
    
    @property
    def capacity(self):
        return self.maxCapacity - len(self.items)

    def addItem(self, item: InventoryItem):
        self.items.append(item)

    def removeItem(self, item: InventoryItem):
        self.items.remove(item)