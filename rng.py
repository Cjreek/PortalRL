from typing import Iterable
import numpy

class RNG:
    def __init__(self, seed: int = None) -> None:
        self.__rng = numpy.random.Generator(numpy.random.PCG64DXSM(seed))
    
    def randint(self, min, max):
        return self.__rng.integers(min, max, endpoint=True)

    def randrange(self, min, max):
        return self.__rng.integers(min, max)

    def choice(self, list: Iterable):
        return list[self.randrange(0, len(list))]

    def random(self):
        return self.__rng.random()