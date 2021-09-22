import esper

from game import Game
from actions.action import Action
from components.melee import Melee
from components.damageable import Damageable
from components.info import Info
from components.level import Level

class FightingAction(Action):
    def __init__(self, x: int, y: int, defenderEntity, costModifier: int = 0) -> None:
        super().__init__(costModifier)
        self.targetX = x
        self.targetY = y
        self.defenderEntity = defenderEntity

    def getPointCost(self) -> int:
        return 5

    def attackEntity(self, game: Game, world: esper.World, level: Level, attackerEntity, defenderEntity):
        attackerInfo: Info = world.try_component(attackerEntity, Info)
        defenderInfo: Info = world.try_component(defenderEntity, Info)

        if self.defenderEntity in level.entitiesAt(self.targetX, self.targetY, True):
            attackerMelee = world.try_component(attackerEntity, Melee)
            defenderDamageable = world.try_component(defenderEntity, Damageable)
            if (attackerMelee) and (defenderDamageable) and (attackerInfo.faction != defenderInfo.faction):
                defenderDamageable.takeDamage(attackerMelee.damage)
                game.logMessage(f"{attackerInfo.name} hits {defenderInfo.name} for {attackerMelee.damage}")
                if defenderDamageable.isDead:
                    game.logMessage(f"{attackerInfo.name} kills {defenderInfo.name}")
        else:
            game.logMessage(f"{defenderInfo.name} dodges {attackerInfo.name}'s attack!")

    def perform(self, game: Game, world: esper.World, level: Level, entity):
        self.attackEntity(game, world, level, entity, self.defenderEntity)