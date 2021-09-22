import esper

from rng import RNG
from game import Game
from ai import AIClass
from actions import MovementAction, FightingAction, Action, WaitAction
from components import Actor, Damageable, Position, Level, Info
from data.enums import Faction

class RandomMonsterAI(AIClass):
    def getDirectionalAction(self, world: esper.World, level: Level, ownFaction: Faction, position: Position, dx: int, dy: int):
        for entity in level.entitiesAt(position.X + dx, position.Y + dy, True):
            info: Info
            info, damageable = world.try_components(entity, Info, Damageable)
            if ((info and damageable) and (info.faction != ownFaction)):
                return FightingAction(position.X + dx, position.Y + dy, entity)

        return MovementAction(dx, dy, costModifier=-2)

    def process(self, entity, actor: Actor, level: Level, game: Game, world: esper.World, rng: RNG):
        entityInfo = world.component_for_entity(entity, Info)
        position = world.component_for_entity(entity, Position)

        dx, dy = rng.randint(-1, 1), rng.randint(-1, 1)
        
        action: Action = None
        if (dx == 0) and (dy == 0):
            action = WaitAction(actor.actionPoints)
        else:
            action = self.getDirectionalAction(world, level, entityInfo.faction, position, dx, dy)
        actor.queueAction(action)

        return True