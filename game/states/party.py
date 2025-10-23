from __future__ import annotations

import itertools

import pygame

from game import settings
from game.core.entities import PlayerCharacter, generate_party
from game.state_machine import GameState


class PartyManagementState(GameState):
    def __init__(self, app: "GameApp") -> None:
        super().__init__(app)
        self.font = pygame.font.Font(settings.FONT_PATH, 28)
        self.small_font = pygame.font.Font(settings.FONT_PATH, 20)
        self.index = 0

    def enter(self, **params) -> None:
        if not self.app.player_party:
            self.app.player_party = generate_party()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                self.app.state_machine.switch("menu")
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.index = (self.index - 1) % len(self.app.player_party)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.index = (self.index + 1) % len(self.app.player_party)
            elif event.key == pygame.K_r:
                self.app.player_party = generate_party()
                self.index = 0

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((10, 14, 24))
        title = self.font.render("Party Concourse", True, settings.WHITE)
        surface.blit(title, (80, 60))
        instructions = "←/→ cycle members | R re-roll squad | ESC return"
        surface.blit(self.small_font.render(instructions, True, settings.LIGHT_GREY), (80, 110))
        for i, member in enumerate(self.app.player_party):
            rect = pygame.Rect(80 + i * 380, 160, 340, 420)
            pygame.draw.rect(surface, (24, 30, 44), rect, border_radius=12)
            border = settings.ACCENT if i == self.index else settings.LIGHT_GREY
            pygame.draw.rect(surface, border, rect, 3)
            header = self.font.render(member.codename, True, settings.WHITE)
            surface.blit(header, (rect.x + 20, rect.y + 20))
            role = self.small_font.render(f"Role: {member.archetype.role}", True, settings.LIGHT_GREY)
            surface.blit(role, (rect.x + 20, rect.y + 70))
            traits = ", ".join(member.archetype.traits)
            trait_text = wrap_text(traits, self.small_font, rect.width - 40)
            for j, line in enumerate(trait_text):
                surface.blit(
                    self.small_font.render(line, True, settings.ACCENT),
                    (rect.x + 20, rect.y + 120 + j * 24),
                )
            strengths = wrap_text("Strengths: " + ", ".join(member.archetype.strengths), self.small_font, rect.width - 40)
            weaknesses = wrap_text("Weaknesses: " + ", ".join(member.archetype.weaknesses), self.small_font, rect.width - 40)
            offset = rect.y + 210
            for line in strengths:
                surface.blit(self.small_font.render(line, True, settings.WHITE), (rect.x + 20, offset))
                offset += 24
            offset += 12
            for line in weaknesses:
                surface.blit(self.small_font.render(line, True, settings.ERROR), (rect.x + 20, offset))
                offset += 24
            ability_header = self.small_font.render("Signature: " + member.archetype.signature_skill, True, settings.ACCENT)
            surface.blit(ability_header, (rect.x + 20, rect.y + 360))


def wrap_text(text: str, font: pygame.font.Font, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    while words:
        current.append(words.pop(0))
        if font.size(" ".join(current))[0] > width:
            current.pop()
            lines.append(" ".join(current))
            current = []
    if current:
        lines.append(" ".join(current))
    return lines
