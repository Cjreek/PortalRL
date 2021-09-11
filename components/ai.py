from random import Random
from ai import AIClass

class AI:
    def __init__(self, initiative: int, aiClass: AIClass, startsReady: bool = False) -> None:
        self.maxInitiative = initiative
        if startsReady:
            self.initiative = 0
        else:
            self.initiative = initiative
        self.aiClass = aiClass
        self.rng = Random() # TODO: muss geseedet sein

    def tickInitiative(self):
        if self.initiative > 0:
            self.initiative -= 1

    def resetInitiative(self):
        self.initiative = self.maxInitiative

    @property
    def isReady(self) -> bool:
        return self.initiative <= 0