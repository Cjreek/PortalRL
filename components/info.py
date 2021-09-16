from data.enums import Faction

class Info:
    def __init__(self, name: str, faction: Faction = Faction.ENEMY) -> None:
        self.name = name
        self.faction = faction