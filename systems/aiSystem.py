from game import Game
from systems.baseSystem import BaseSystem
from components import AI, Actor

# (AI)
class AISystem(BaseSystem):
    def __init__(self) -> None:
        super().__init__()
        self.waitingFor = []

    def reset(self):
        self.waitingFor = []
    
    def executeEntityActions(self, game: Game, entity, actor: Actor, ai: AI):
        while (actor.actionPoints > 0) and ((actor.currentAction) or (ai.aiClass.process(entity, actor, game, self.world, ai.rng))):
            while (actor.currentAction) and (actor.actionPoints > 0):
                points = min(actor.actionPoints, actor.currentAction.remainingCost)
                actor.actionPoints -= points
                actor.currentAction.remainingCost -= points
                if actor.currentAction.remainingCost == 0:
                    actor.currentAction.perform(game, self.world, entity)
                    actor.nextAction()       

    def execute(self, game: Game, *args, **kwargs):
        ai: AI
        actor: Actor
        if (len(self.waitingFor) > 0):
            for item in self.waitingFor:
                entity, (ai, actor) = item
                if not self.world.entity_exists(entity):
                    self.waitingFor.remove(item)
                else:
                    self.executeEntityActions(game, entity, actor, ai)
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
                        self.executeEntityActions(game, entity, actor, ai)
                        if actor.actionPoints == 0:
                            actor.resetInitiative()
                            actor.resetActionPoints()
                        else:
                            self.waitingFor.append((entity, (ai, actor)))
                            waitingForAction = True