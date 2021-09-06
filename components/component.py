from __future__ import annotations
from typing import TypeVar, TYPE_CHECKING

import imports
if TYPE_CHECKING:
    from entity import Entity

class Component:
    def __init__(self, tickAlways = False, parent: Entity = None) -> None:
        self.parent: Entity = parent
        self.tickAlways = tickAlways

    def beforeRender(self):
        pass

    def tick(self) -> bool:
        return True

    @property
    def Type():
        return TypeVar("T", bound=Component)

