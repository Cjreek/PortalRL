import esper

from game import Game
from actions.action import Action
from components.melee import Melee
from components.damageable import Damageable
from components.info import Info
from components.level import Level

class FightingAction(Action):
    def __init__(self, defenderEntity, costModifier: int = 0) -> None:
        super().__init__(costModifier)
        self.defenderEntity = defenderEntity

    def getPointCost(self) -> int:
        return 5

    def attackEntity(self, game: Game, world: esper.World, attackerEntity, defenderEntity):
        attackerMelee = world.try_component(attackerEntity, Melee)
        attackerInfo: Info = world.try_component(attackerEntity, Info)
        world.try_component(attackerEntity, Melee)
        
        defenderDamageable = world.try_component(defenderEntity, Damageable)
        defenderInfo: Info = world.try_component(defenderEntity, Info)
        if (attackerMelee) and (defenderDamageable) and (attackerInfo.faction != defenderInfo.faction):
            defenderDamageable.takeDamage(attackerMelee.damage)
            game.logMessage(f"{attackerInfo.name} hits {defenderInfo.name} for {attackerMelee.damage}")
            if defenderDamageable.isDead:
                game.logMessage(f"{attackerInfo.name} kills {defenderInfo.name}")

    def perform(self, game: Game, world: esper.World, level: Level, entity):
        self.attackEntity(game, world, entity, self.defenderEntity)