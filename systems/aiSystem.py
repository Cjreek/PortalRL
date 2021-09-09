import esper

from components import AI

# (AI)
class AISystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
        self.world: esper.World = self.world
        self.waitingFor = []
    
    def process(self, *args, **kwargs):
        ai: AI
        if (len(self.waitingFor) > 0):
            for item in self.waitingFor:
                entity, ai = item
                if not self.world.entity_exists(entity):
                    self.waitingFor.remove(item)
                elif ai.aiClass.process(entity, self.world, ai.rng):
                    ai.resetInitiative()
                    self.waitingFor.remove(item)
        else:
            entityList = self.world.get_component(AI)
            waitingForAction = False
            while (not waitingForAction):
                for entity, ai in entityList:
                    ai.tickInitiative()
                    if (ai.isReady):
                        if ai.aiClass.process(entity, self.world, ai.rng):
                            ai.resetInitiative()
                        else:
                            self.waitingFor.append((entity, ai))
                            waitingForAction = True