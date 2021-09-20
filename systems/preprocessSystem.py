from components.blocking import Blocking
from components.position import Position
from game import Game
from systems.baseSystem import BaseSystem
from components import Level

class PreprocessSystem(BaseSystem):
    def execute(self, game: Game, *args, **kwargs):
        level: Level
        _, level = self.world.get_component(Level)[0]

        position: Position
        level.entities.clear()
        for entity, position in self.world.get_component(Position):
            position.setDirty(False)
            pt = (position.X, position.Y)
            entityList = level.entities.get(pt, None) or []
            entityList.append(entity)
            level.entities[pt] = entityList
        
        level.blockingEntities.clear()
        for entity, (position, _) in self.world.get_components(Position, Blocking):
            pt = (position.X, position.Y)
            entityList = level.blockingEntities.get(pt, None) or []
            entityList.append(entity)
            level.blockingEntities[pt] = entityList