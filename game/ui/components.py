from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Tuple

import pygame

from game import settings


@dataclass
class Button:
    label: str
    rect: pygame.Rect
    callback: Callable[[], None]
    description: str = ""

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, hover: bool = False) -> None:
        color = settings.ACCENT if hover else settings.LIGHT_GREY
        pygame.draw.rect(surface, color, self.rect, border_radius=8, width=2)
        text_surf = font.render(self.label, True, color)
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def contains(self, pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)


class GridRenderer:
    def __init__(self, tile_size: int = settings.GRID_SIZE) -> None:
        self.tile_size = tile_size
        self.floor_color = (48, 62, 71)
        self.wall_color = (18, 28, 36)
        self.grid_color = (32, 42, 52)

    def draw(self, surface: pygame.Surface, grid: List[List[int]]) -> None:
        surface.fill((12, 16, 24))
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                color = self.floor_color if value == 0 else self.wall_color
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, self.grid_color, rect, 1)
