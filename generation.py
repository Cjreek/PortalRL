from __future__ import annotations

from typing import Iterator, Tuple
import random

import esper
import tcod
import pyperclip

from data import tiles, mobs, items
from components import Level, Position
    
class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x1 = x
        self.y1 = y
        self.width = width
        self.height = height

    @property 
    def x2(self) -> int:
        return self.x1 + self.width
    
    @property 
    def y2(self) -> int:
        return self.y1 + self.height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y 

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1, self.x2), slice(self.y1, self.y2) # x1/y1 + 1 ?

    def inBounds(self, x1: int, y1: int, width: int, height: int) -> bool:
        x2 = x1 + width
        y2 = y1 + height
        return (self.x1 >= x1) and (self.x2 <= x2) and (self.y1 >= y1) and (self.y2 <= y2)

    def intersects(self, otherRoom: RectangularRoom) -> bool:
        return (self.x1 <= otherRoom.x2) and (self.x2 >= otherRoom.x1) and (self.y1 <= otherRoom.y2) and (self.y2 >= otherRoom.y1)

def makeCorridor(rng: random.Random, start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end
    if rng.random() < 0.5:
        cornerX, cornerY = x2, y1
    else:
        cornerX, cornerY = x1, y2

    for x, y in tcod.los.bresenham((x1, y1), (cornerX, cornerY)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((cornerX, cornerY), (x2, y2)).tolist():
        yield x, y

def generateLevel(world: esper.World, level: Level, playerPos: Position, minRoomSize: int, maxRoomSize: int,minRoomCount: int, maxRoomCount: int) -> Level:
    ### DEBUG ###
    pyperclip.copy(str(level.seed))
    #############
    
    fails = 0
    numRooms = level.rng.randint(minRoomCount, maxRoomCount)
    while (numRooms > 0) and (fails < 10):
        newRoom = RectangularRoom(x=level.rng.randrange(0, level.width), y=level.rng.randrange(0, level.height), width=level.rng.randint(minRoomSize, maxRoomSize), height=level.rng.randint(minRoomSize, maxRoomSize))
        
        newRoomFails = 0
        failed = False
        while(newRoomFails < 10):
            failed = not newRoom.inBounds(1, 1, level.width-2, level.height-2) or any(newRoom.intersects(room) for room in level.rooms)
            if failed:
                newRoom.x1 = level.rng.randrange(0, level.width)
                newRoom.y1 = level.rng.randrange(0, level.height)
                newRoomFails += 1
            else:
                break 

        if not failed:
            level.rooms.append(newRoom)

            if len(level.rooms) > 1:
                # Mobs 
                numMobs = level.rng.randint(5, 8)
                for _ in range(numMobs):
                    mobs.spawn(world, level.rng.choice(mobs.MOBLIST), level.rng.randint(newRoom.x1+1, newRoom.x2-1), level.rng.randint(newRoom.y1+1, newRoom.y2-1))

                # Items
                numItems = level.rng.randint(0, 1)
                for _ in range(numItems):
                    items.spawn(world, level.rng.choice(items.ITEMPOOL), level.rng.randint(newRoom.x1+1, newRoom.x2-1), level.rng.randint(newRoom.y1+1, newRoom.y2-1))
                    
            if len(level.rooms) > 1:
                for x, y in makeCorridor(level.rng, level.rooms[-2].center, newRoom.center):
                    level.tiles[x, y] = tiles.floor

            numRooms -= 1
            fails = 0
        else:
            fails += 1

    # room decorations
    for room in level.rooms:
        level.tiles[room.inner] = level.rng.choice(tiles.floortiles)

    playerPos.X, playerPos.Y = level.rooms[0].center