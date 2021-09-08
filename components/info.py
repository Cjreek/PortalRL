from data import factions

class Info:
    def __init__(self, name: str, faction: int = factions.ENEMY) -> None:
        self.name = name
        self.faction = faction