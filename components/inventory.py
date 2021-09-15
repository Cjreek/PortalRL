class Inventory:
    idCounter: int = 1

    def __init__(self, maxCapacity: int) -> None:
        self.maxCapacity = maxCapacity
        self.items = []
        self.id = Inventory.idCounter 
        Inventory.idCounter += 1