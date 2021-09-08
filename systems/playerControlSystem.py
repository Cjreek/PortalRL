import esper

from components import Player, Input, Velocity

# (Player, Input, Velocity)
class PlayerControlSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
        self.world: esper.World = self.world

    def process(self, *args, **kwargs):
        input: Input
        velocity: Velocity
        for _, (_, input, velocity) in self.world.get_components(Player, Input, Velocity):
            velocity.dx = 0
            velocity.dy = 0
            if (input.Up): velocity.dy = -1
            if (input.Down): velocity.dy = 1
            if (input.Left): velocity.dx = -1
            if (input.Right): velocity.dx = 1
            if (input.UpLeft): velocity.dy, velocity.dx = -1, -1
            if (input.UpRight): velocity.dy, velocity.dx = -1, 1
            if (input.DownLeft): velocity.dy, velocity.dx = 1, -1
            if (input.DownRight): velocity.dy, velocity.dx = 1, 1
            if (input.Escape): raise SystemExit()
            