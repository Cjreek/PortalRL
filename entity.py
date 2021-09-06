from __future__ import annotations
from components.lightsource import LightSource
from typing import TYPE_CHECKING

from typing import Tuple, List, Optional
import copy

from tcod.console import Console

import imports
if TYPE_CHECKING:
    from imports import color
    from imports import lighting
    from imports import factions
    from imports import renderprio
    from components.lightsource import LightSource
    from components.actor import Actor
    from level import Level
    from components.component import Component
    
class Entity:
    def __init__(self, name: str, char: str, color: Tuple[int, int, int], components: List[Component] = [], faction: int = factions.ENEMIES, hasCollider: bool = True, renderPrio: int = renderprio.NORMAL, level: Optional[Level] = None, x: int = 0, y: int = 0):
        self.name = name
        self.char = char
        self.color = color
        self.level = level
        self.x = x
        self.y = y
        self.renderPrio = renderPrio
        self.faction = faction
        self.hasCollider = hasCollider
        self.lightsource: LightSource = None
        self.actorComponent = None
        self.components: List[component.Component] = []
        for component in components:
            self.addComponent(component)

    def getComponents(self, type: Component.Type) -> List[Component.Type]:
        return list((item for item in self.components if isinstance(item, type)))

    def getComponent(self, type: Component.Type):
        list = self.getComponents(type)
        if len(list) > 0:
            return list[0]
        return None
    
    @property
    def actor(self):
        if not self.actorComponent:
            self.actorComponent = self.getComponent(Actor)
        return self.actorComponent

    @property
    def fov(self):
        if not (self.lightsource):
            self.lightsource = self.getComponent(LightSource)

        if (self.lightsource):
            if len(self.lightsource.fov) == 0:
                self.lightsource.update()
            return self.lightsource.fov
        else:
            return None

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def beforeRender(self):
        for component in self.components:
            component.beforeRender()

    def tick(self, onlyAlways = False):
        result = True
        for component in self.components:
            if (not onlyAlways) or (component.tickAlways):
                result = result and component.tick()
        return result

    def render(self, console: Console):
        if self.level.engine.useLighting:
            hsl = color.toHLS(self.color)
            hsl = (hsl[0], hsl[1] * (self.level.lighting["level"][self.x, self.y][0] / lighting.MAX_LIGHT_LEVEL), hsl[2])
            rgb = color.toRGB(hsl)
            rgb = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
            self.level.print(console, self.x, self.y, self.char, rgb)
        else:
            self.level.print(console, self.x, self.y, self.char, self.color)

    def spawn(self, level: Level, x: int, y: int) -> Entity:
        spawnEntity = copy.deepcopy(self)
        spawnEntity.x = x
        spawnEntity.y = y
        level.addEntity(spawnEntity)
        return spawnEntity

    def addComponent(self, component: Component):
        self.components.append(component)
        component.parent = self

        if isinstance(component, LightSource):
            self.lightsource = component

    def removeComponent(self, component: Component):
        component.parent = None
        self.components.remove(component)

        if isinstance(component, LightSource):
            self.lightsource = None