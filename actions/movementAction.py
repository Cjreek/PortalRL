import esper

from game import Game
from components.level import Level
from components.position import Position
from components.fov import FOV
from components.light import Light

from actions.action import Action

class MovementAction(Action):
    def __init__(self, dx: int, dy: int, costModifier: int = 0) -> None:
        super().__init__(costModifier)
        self.dx = dx
        self.dy = dy

    def getPointCost(self) -> int:
        return 5

    def moveEntity(self, world: esper.World, entity, position: Position, destX: int, destY: int):
        position.X = destX
        position.Y = destY
        # TODO: move to somewhere else?
        if world.has_component(entity, FOV):
            fov = world.component_for_entity(entity, FOV)
            fov.dirty = True
        if world.has_component(entity, Light):
            light = world.component_for_entity(entity, Light)
            light.dirty = True
        
    def perform(self, game: Game, world: esper.World, level: Level, entity):
        position = world.component_for_entity(entity, Position)

        destX = position.X + self.dx
        destY = position.Y + self.dy
        if level.isWalkable(destX, destY):
            level.reportEntityMovement(entity, (position.X, position.Y), (destX, destY))
            self.moveEntity(world, entity, position, destX, destY)