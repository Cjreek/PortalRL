import esper

from rng import RNG
from game import Game, GameState
from ai import AIClass
from components import Input, Actor, Level, Position, Damageable
from actions import MovementAction, WaitAction, FightingAction

class PlayerController(AIClass):
    def getDirectionalAction(self, world: esper.World, level: Level, position: Position, dx: int, dy: int):
        tileEntities = level.entitiesAt(position.X + dx, position.Y + dy, True)
        
        defenderEntity = None
        for entity in tileEntities:
            if world.has_component(entity, Damageable):
                defenderEntity = entity
                break

        if defenderEntity:
            return FightingAction(defenderEntity)
        else:
            return MovementAction(dx, dy, costModifier=-2)

    def process(self, entity, actor: Actor, game: Game, world: esper.World, rng: RNG):
        input = world.component_for_entity(entity, Input)
        position = world.component_for_entity(entity, Position)
        _, level = world.get_component(Level)[0]
        
        result = False
        if game.state == GameState.PLAYING:
            result = True
            action = None
            if (input.Up): action = self.getDirectionalAction(world, level, position, 0, -1)
            elif (input.Down): action = self.getDirectionalAction(world, level, position, 0, 1)
            elif (input.Left): action = self.getDirectionalAction(world, level, position, -1, 0)
            elif (input.Right): action = self.getDirectionalAction(world, level, position, 1, 0)
            elif (input.UpLeft): action =  self.getDirectionalAction(world, level, position, -1, -1)
            elif (input.UpRight): action = self.getDirectionalAction(world, level, position, 1, -1)
            elif (input.DownLeft): action = self.getDirectionalAction(world, level, position, -1, 1)
            elif (input.DownRight): action = self.getDirectionalAction(world, level, position, 1, 1)
            elif (input.Wait): action = WaitAction(actor.actionPoints)
            else: result = False

            if action:
                input.clear()
                actor.queueAction(action)
        
        if (input.inventoryKey):
            if game.state == GameState.PLAYING:
                game.changeState(GameState.INVENTORY)
            elif game.state == GameState.INVENTORY:
                game.changeState(GameState.PLAYING)
        if (input.Escape): 
            if game.state == GameState.INVENTORY:
                game.changeState(GameState.PLAYING)
            elif game.state == GameState.PLAYING:
                game.changeState(GameState.MAINMENU)

        return result