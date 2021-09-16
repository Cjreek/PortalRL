from components.item import Item

class InventoryItem:
    def __init__(self, entity, item: Item) -> None:
        self.entity = entity
        self.itemData = item