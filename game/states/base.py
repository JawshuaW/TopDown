from __future__ import annotations

from typing import List, Tuple

import pygame

from game import settings


class MenuOption:
    def __init__(self, text: str, callback, description: str = "") -> None:
        self.text = text
        self.callback = callback
        self.description = description


class BaseMenuState:
    def __init__(self, app: "GameApp") -> None:
        self.app = app
        self.options: List[MenuOption] = []
        self.index = 0
        self.title = ""
        self.subtitle = ""
        self.font = pygame.font.Font(settings.FONT_PATH, 32)
        self.large_font = pygame.font.Font(settings.FONT_PATH, 48)
        self.small_font = pygame.font.Font(settings.FONT_PATH, 24)

    def enter(self, **params) -> None:
        self.index = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.index = (self.index - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.index = (self.index + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.options[self.index].callback()

    def update(self, dt: float) -> None:  # pragma: no cover - mostly rendering
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(settings.BLACK)
        title_surf = self.large_font.render(self.title, True, settings.WHITE)
        surface.blit(title_surf, title_surf.get_rect(center=(settings.WINDOW_WIDTH // 2, 100)))

        if self.subtitle:
            subtitle = self.small_font.render(self.subtitle, True, settings.LIGHT_GREY)
            surface.blit(
                subtitle,
                subtitle.get_rect(center=(settings.WINDOW_WIDTH // 2, 160)),
            )

        base_y = 240
        for i, option in enumerate(self.options):
            color = settings.ACCENT if i == self.index else settings.WHITE
            option_surf = self.font.render(option.text, True, color)
            rect = option_surf.get_rect(center=(settings.WINDOW_WIDTH // 2, base_y + i * 60))
            surface.blit(option_surf, rect)
            if option.description and i == self.index:
                self._draw_description(surface, option.description)

    def _draw_description(self, surface: pygame.Surface, description: str) -> None:
        wrapped = wrap_text(description, self.small_font, settings.WINDOW_WIDTH - 200)
        for i, line in enumerate(wrapped):
            surf = self.small_font.render(line, True, settings.LIGHT_GREY)
            surface.blit(surf, (120, 480 + i * 26))


def wrap_text(text: str, font: pygame.font.Font, width: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current: List[str] = []
    while words:
        current.append(words.pop(0))
        if font.size(" ".join(current))[0] > width:
            current.pop()
            lines.append(" ".join(current))
            current = []
    if current:
        lines.append(" ".join(current))
    return lines
