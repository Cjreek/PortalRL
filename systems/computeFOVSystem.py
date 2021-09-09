import esper
from tcod.map import compute_fov
import tcod.constants

from components import Position, FOV, Level

# (Level), (Position, FOV)
class ComputeFOVSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
        self.world: esper.World = self.world

    def process(self, *args, **kwargs):
        position: Position
        fov: FOV
        level: Level
        _, level = self.world.get_component(Level)[0]
        for _, (position, fov) in self.world.get_components(Position, FOV):
            if (fov.dirty):
                # fov.fov = compute_fov(level.tiles["transparent"], (position.X, position.Y), radius=fov.viewDistance)
                fov.fov = compute_fov(level.tiles["transparent"], (position.X, position.Y), radius=fov.viewDistance, algorithm=tcod.constants.FOV_BASIC)
                fov.dirty = False