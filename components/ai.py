from rng import RNG

class AI:
    def __init__(self, aiClass: "AIClass") -> None:
        self.aiClass = aiClass
        self.rng = RNG() # TODO: muss geseedet sein