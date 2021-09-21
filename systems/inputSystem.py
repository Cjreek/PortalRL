from tcod.context import Context
import tcod.event

from game import Game
from systems.baseSystem import BaseSystem
from components import Input, Level
from data import layout

# (Input)
class InputSystem(BaseSystem):
    def __init__(self, context: Context) -> None:
        super().__init__()
        self.context = context

    def execute(self, game: Game, level: Level):
        input: Input

        for _, input in self.world.get_component(Input):
            input.clear()

        for event in tcod.event.get():
            self.context.convert_event(event)

            if isinstance(event, tcod.event.Quit):
                raise SystemExit()

            if isinstance(event, tcod.event.MouseMotion):
                event: tcod.event.MouseMotion
                for _, input in self.world.get_component(Input):
                    input.MouseX, input.MouseY = event.tile
                    input.MouseLevelX = input.MouseX - layout.LEVEL_OFFSET_X
                    input.MouseLevelY = input.MouseY - layout.LEVEL_OFFSET_Y

            if isinstance(event, tcod.event.KeyDown):
                event: tcod.event.KeyDown
               
                key = event.sym

                up = key in (tcod.event.K_UP, tcod.event.K_KP_8, tcod.event.K_k)
                down = key in (tcod.event.K_DOWN, tcod.event.K_KP_2, tcod.event.K_j)
                left = key in (tcod.event.K_LEFT, tcod.event.K_KP_4, tcod.event.K_h)
                right = key in (tcod.event.K_RIGHT, tcod.event.K_KP_6, tcod.event.K_l)
                upLeft = key in (tcod.event.K_KP_7, tcod.event.K_y, tcod.event.K_z)
                upRight = key in (tcod.event.K_KP_9, tcod.event.K_u)
                downLeft = key in (tcod.event.K_KP_1, tcod.event.K_b)
                downRight = key in (tcod.event.K_KP_3, tcod.event.K_n)
                wait = key in (tcod.event.K_KP_5, tcod.event.K_PLUS)
                drop = (key == tcod.event.K_d)
                equip = (key == tcod.event.K_e)
                escape = (key == tcod.event.K_ESCAPE) and not (event.repeat)

                inventoryKey = (key == tcod.event.K_i) and not (event.repeat)

                debug = (key >= tcod.event.K_F1) and (key <= tcod.event.K_F12) and not (event.repeat)

                for _, input in self.world.get_component(Input):
                    input.Up = up
                    input.Down = down
                    input.Left = left
                    input.Right = right
                    input.UpLeft = upLeft
                    input.UpRight = upRight
                    input.DownLeft = downLeft
                    input.DownRight = downRight
                    input.Wait = wait
                    input.Drop = drop
                    input.Equip = equip
                    input.Escape = escape

                    input.inventoryKey = inventoryKey

                    input.Debug = debug
                    input.RawKey = key