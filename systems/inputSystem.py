import esper
import tcod.event

from components import Input

# (Input)
class InputSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
        self.world: esper.World = self.world

    def process(self, *args, **kwargs):
        input: Input
        for _, input in self.world.get_component(Input):
            input.clear()

        for event in tcod.event.get():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()

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
                escape = key == tcod.event.K_ESCAPE
                debug = (key >= tcod.event.K_F1) and (key <= tcod.event.K_F12)

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
                    input.Escape = escape
                    input.Debug = debug
                    input.DebugKey = key