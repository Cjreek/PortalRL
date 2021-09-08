import esper

from components import AI

# (AI)
class AISystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
        self.world: esper.World = self.world
    
    def process(self, *args, **kwargs):
        ai: AI
        for entity, ai in self.world.get_component(AI):
            ai.tickInitiative()
            if ai.isReady:
                ai.aiClass.process(entity, self.world, ai.rng)
                ai.resetInitiative()