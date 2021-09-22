from components.damageable import Damageable
from game import Game
from systems.baseSystem import BaseSystem
from components import AI, Actor, Level, Player

# (AI)
class AISystem(BaseSystem):
    def __init__(self) -> None:
        super().__init__()
        self.waitingFor = []

    def reset(self):
        self.waitingFor.clear()
    
    # TODO: dead players being able to perform actions is a workaround so that keyboard controls still work
    def canPerformActions(self, entity) -> bool:
        damageable = self.world.try_component(entity, Damageable)
        return (not damageable) or (not damageable.isDead) or (damageable.isDead and self.world.has_component(entity, Player)) 

    def executeEntityActions(self, game: Game, level: Level, entity, actor: Actor, ai: AI):
        if self.canPerformActions(entity):
            while (actor.actionPoints > 0) and ((actor.currentAction) or (ai.aiClass.process(entity, actor, level, game, self.world, ai.rng))):
                while (actor.currentAction) and (actor.actionPoints > 0):
                    points = min(actor.actionPoints, actor.currentAction.remainingCost)
                    actor.actionPoints -= points
                    actor.currentAction.remainingCost -= points
                    if actor.currentAction.remainingCost == 0:
                        actor.currentAction.perform(game, self.world, level, entity)
                        actor.nextAction()       

    def execute(self, game: Game, level: Level):
        ai: AI
        actor: Actor
        if (len(self.waitingFor) > 0):
            for item in self.waitingFor:
                entity, (ai, actor) = item
                if not self.world.entity_exists(entity):
                    self.waitingFor.remove(item)
                else:
                    self.executeEntityActions(game, level, entity, actor, ai)
                    if actor.actionPoints == 0:
                        actor.resetInitiative()
                        actor.resetActionPoints()
                        self.waitingFor.remove(item)
        else:
            entityList = self.world.get_components(AI, Actor)
            waitingForAction = False
            while (not waitingForAction):
                waitingForAction = False
                for entity, (ai, actor) in entityList:
                    actor.tickInitiative()
                    if (actor.isReady) and self.world.entity_exists(entity):
                        self.executeEntityActions(game, level, entity, actor, ai)
                        if actor.actionPoints == 0:
                            actor.resetInitiative()
                            actor.resetActionPoints()
                        else:
                            self.waitingFor.append((entity, (ai, actor)))
                            waitingForAction = True