from __future__ import annotations
from typing import TYPE_CHECKING

from typing import Iterator, Tuple
import random

import tcod
import pyperclip

import imports
if TYPE_CHECKING:
    import tiles
    import mobs
    from level import Level
    from engine import Engine
    from gamestates.game import Game
    
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

    def inBounds(self, x1: int, y1: int, width: int, height: int, debug: bool = False) -> bool:
        x2 = x1 + width
        y2 = y1 + height
        if debug:
            print("Wx1: " + str(x1) + ", Wy1: " + str(y1) + ", Wx2: " + str(x2) + ", wy2: " + str(y2))
            print("Rx1: " + str(self.x1) + ", Ry1: " + str(self.y1) + ", Rx2: " + str(self.x2) + ", Ry2: " + str(self.y2))
            print("--")
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

def generateLevel(minRoomSize: int, maxRoomSize: int,minRoomCount: int, maxRoomCount: int, engine: Engine, game: Game, seed: int = None) -> Level:
    if not seed:
        seed = int.from_bytes(random.randbytes(4), byteorder='little', signed=False)
    pyperclip.copy(str(seed))
    newLevel = Level(engine, game, seed)

    fails = 0
    numRooms = newLevel.rng.randint(minRoomCount, maxRoomCount)
    while (numRooms > 0) and (fails < 10):
        newRoom = RectangularRoom(x=newLevel.rng.randrange(0, newLevel.width), y=newLevel.rng.randrange(0, newLevel.height), width=newLevel.rng.randint(minRoomSize, maxRoomSize), height=newLevel.rng.randint(minRoomSize, maxRoomSize))
        
        newRoomFails = 0
        failed = False
        while(newRoomFails < 10):
            failed = not newRoom.inBounds(1, 1, newLevel.width-2, newLevel.height-2) or any(newRoom.intersects(room) for room in newLevel.rooms)
            if failed:
                newRoom.x1 = newLevel.rng.randrange(0, newLevel.width)
                newRoom.y1 = newLevel.rng.randrange(0, newLevel.height)
                newRoomFails += 1
            else:
                break 

        if not failed:
            newLevel.rooms.append(newRoom)
            newLevel.tiles[newRoom.inner] = newLevel.rng.choice(tiles.floortiles) #tiles.floor if level.rng.random() < 0.5 else tiles.grass

            # Mobs
            numMobs = newLevel.rng.randint(0, 3) #4
            for _ in range(numMobs):
                mobToSpawn = newLevel.rng.choice(mobs.MOBLIST)
                mobToSpawn.spawn(newLevel, newLevel.rng.randint(newRoom.x1+1, newRoom.x2-1), newLevel.rng.randint(newRoom.y1+1, newRoom.y2-1))

            if len(newLevel.rooms) > 1:
                for x, y in makeCorridor(newLevel.rng, newLevel.rooms[-2].center, newRoom.center):
                    newLevel.tiles[x, y] = tiles.floor

            numRooms -= 1
            fails = 0
        else:
            fails += 1

    game.player.x, game.player.y = newLevel.rooms[0].center
    newLevel.addEntity(game.player)

    return newLevel