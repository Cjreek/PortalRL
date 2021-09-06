from __future__ import annotations
from typing import TYPE_CHECKING

from typing import Optional

import tcod.event

import imports
if TYPE_CHECKING:
    from actions import Action, MovementAction, CancelAction, DebugAction
    from engine import Engine

class EventHandler(tcod.event.EventDispatch[Action]):

    def __init__(self, engine: Engine) -> None:
        super().__init__()
        self.engine = engine

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        # Movement
        if key in (tcod.event.K_UP, tcod.event.K_KP_8, tcod.event.K_k):
            action = MovementAction(dx=0, dy=-1)
        elif key in (tcod.event.K_DOWN, tcod.event.K_KP_2, tcod.event.K_j):
            action = MovementAction(dx=0, dy=1)
        elif key in (tcod.event.K_LEFT, tcod.event.K_KP_4, tcod.event.K_h):
            action = MovementAction(dx=-1, dy=0)
        elif key in (tcod.event.K_RIGHT, tcod.event.K_KP_6, tcod.event.K_l):
            action = MovementAction(dx=1, dy=0)
        elif key in (tcod.event.K_KP_7, tcod.event.K_y, tcod.event.K_z):
            action = MovementAction(dx=-1, dy=-1)
        elif key in (tcod.event.K_KP_9, tcod.event.K_u):
            action = MovementAction(dx=1, dy=-1)
        elif key in (tcod.event.K_KP_1, tcod.event.K_b):
            action = MovementAction(dx=-1, dy=1)
        elif key in (tcod.event.K_KP_3, tcod.event.K_n):
            action = MovementAction(dx=1, dy=1)
        elif key in (tcod.event.K_KP_5, tcod.event.K_PLUS): # PLUS?
            action = MovementAction(dx=0, dy=0)

        # Cancel
        elif key == tcod.event.K_ESCAPE:
            action = CancelAction()
        # Debug
        elif (key >= tcod.event.K_F1) and (key <= tcod.event.K_F12):
            action = DebugAction(key)

        return action