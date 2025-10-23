from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Tuple

from game import settings


TILE_WALL = 1
TILE_FLOOR = 0


@dataclass
class Room:
    x: int
    y: int
    width: int
    height: int

    def center(self) -> Tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)

    def intersects(self, other: "Room") -> bool:
        return not (
            self.x + self.width < other.x
            or self.x > other.x + other.width
            or self.y + self.height < other.y
            or self.y > other.y + other.height
        )


def carve_room(grid: List[List[int]], room: Room) -> None:
    for x in range(room.x, room.x + room.width):
        for y in range(room.y, room.y + room.height):
            if 0 <= x < settings.DUNGEON_WIDTH and 0 <= y < settings.DUNGEON_HEIGHT:
                grid[y][x] = TILE_FLOOR


def carve_hallway(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> None:
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        carve_horizontal(grid, x1, x2, y1)
        carve_vertical(grid, y1, y2, x2)
    else:
        carve_vertical(grid, y1, y2, x1)
        carve_horizontal(grid, x1, x2, y2)


def carve_horizontal(grid: List[List[int]], x1: int, x2: int, y: int) -> None:
    for x in range(min(x1, x2), max(x1, x2) + 1):
        if 0 <= x < settings.DUNGEON_WIDTH and 0 <= y < settings.DUNGEON_HEIGHT:
            grid[y][x] = TILE_FLOOR


def carve_vertical(grid: List[List[int]], y1: int, y2: int, x: int) -> None:
    for y in range(min(y1, y2), max(y1, y2) + 1):
        if 0 <= x < settings.DUNGEON_WIDTH and 0 <= y < settings.DUNGEON_HEIGHT:
            grid[y][x] = TILE_FLOOR


def generate_dungeon(seed: int | None = None) -> Tuple[List[List[int]], List[Room]]:
    rng = random.Random(seed)
    grid = [[TILE_WALL for _ in range(settings.DUNGEON_WIDTH)] for _ in range(settings.DUNGEON_HEIGHT)]
    rooms: List[Room] = []

    for _ in range(10):
        w = rng.randint(3, 6)
        h = rng.randint(3, 5)
        x = rng.randint(1, settings.DUNGEON_WIDTH - w - 1)
        y = rng.randint(1, settings.DUNGEON_HEIGHT - h - 1)
        new_room = Room(x, y, w, h)
        if any(new_room.intersects(other) for other in rooms):
            continue
        carve_room(grid, new_room)
        if rooms:
            prev_center = rooms[-1].center()
            carve_hallway(grid, prev_center, new_room.center())
        rooms.append(new_room)

    return grid, rooms
