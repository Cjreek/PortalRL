from typing import List
class Step:
        def __init__(self, dx: int, dy: int) -> None:
            self.dx = dx
            self.dy = dy
class Velocity:
    def __init__(self) -> None:
        self.steps: List[Step] = []
    
    def addStep(self, dx: int, dy: int):
        self.steps.append(Step(dx,dy))