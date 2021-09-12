from tcod.map import compute_fov
import tcod.constants

from game import Game
from systems.baseSystem import BaseSystem
from components import Position, FOV, Level, Light

# (Level), (Position, FOV)
class ComputeFOVSystem(BaseSystem):
    def execute(self, game: Game, *args, **kwargs):
        position: Position
        fov: FOV
        level: Level
        _, level = self.world.get_component(Level)[0]
        for entity, (position, fov) in self.world.get_components(Position, FOV):
            if (fov.dirty):
                fov.fov = compute_fov(level.tiles["transparent"], (position.X, position.Y), radius=fov.viewDistance, algorithm=tcod.constants.FOV_PERMISSIVE_8)
                light: Light = self.world.try_component(entity, Light)
                if light:
                    fov.lightFov = compute_fov(level.tiles["transparent"], (position.X, position.Y), radius=light.intensity+1, light_walls=False, algorithm=tcod.constants.FOV_DIAMOND)
                fov.dirty = False