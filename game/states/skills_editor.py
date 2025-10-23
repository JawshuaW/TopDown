from __future__ import annotations

from typing import List

import pygame

from game import settings
from game.core.entities import Skill, skill_catalogue
from game.state_machine import GameState
from game.states.base import BaseMenuState, MenuOption


class SkillsEditorState(BaseMenuState, GameState):
    def __init__(self, app: "GameApp") -> None:
        GameState.__init__(self, app)
        BaseMenuState.__init__(self, app)
        self.title = "Skill Laboratory"
        self.subtitle = "Unlock and assign advanced manoeuvres"
        self.catalogue: List[Skill] = skill_catalogue()
        self.selection_font = pygame.font.Font(settings.FONT_PATH, 22)
        self.options = [
            MenuOption("Back", lambda: self.app.state_machine.switch("menu")),
        ]
        self.selected_skill: Skill | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.state_machine.switch("menu")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.selected_skill:
            party_member = self.app.player_party[0] if self.app.player_party else None
            if party_member and self.selected_skill not in party_member.learned_skills:
                party_member.learned_skills.append(self.selected_skill)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

    def handle_click(self, pos) -> None:
        for i, skill in enumerate(self.catalogue):
            rect = pygame.Rect(80, 180 + i * 90, 420, 80)
            if rect.collidepoint(pos):
                self.selected_skill = skill
                break

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(settings.BLACK)
        title = self.large_font.render(self.title, True, settings.WHITE)
        surface.blit(title, (80, 60))
        subtitle = self.small_font.render(self.subtitle, True, settings.LIGHT_GREY)
        surface.blit(subtitle, (80, 120))
        for i, skill in enumerate(self.catalogue):
            rect = pygame.Rect(80, 180 + i * 90, 420, 80)
            pygame.draw.rect(surface, (28, 36, 46), rect, border_radius=8)
            pygame.draw.rect(surface, settings.ACCENT, rect, 2)
            name_surf = self.font.render(skill.name, True, settings.WHITE)
            tier_surf = self.small_font.render(f"Tier {skill.tier}", True, settings.LIGHT_GREY)
            surface.blit(name_surf, (rect.x + 16, rect.y + 12))
            surface.blit(tier_surf, (rect.x + 16, rect.y + 48))
            desc_lines = skill.description.split(" ")
            preview = " ".join(desc_lines[:8]) + ("..." if len(desc_lines) > 8 else "")
            preview_surf = self.small_font.render(preview, True, settings.LIGHT_GREY)
            surface.blit(preview_surf, (rect.x + 220, rect.y + 48))

        if self.selected_skill:
            detail_rect = pygame.Rect(560, 180, 620, 360)
            pygame.draw.rect(surface, (18, 22, 32), detail_rect, border_radius=12)
            pygame.draw.rect(surface, settings.ACCENT, detail_rect, 2)
            name = self.large_font.render(self.selected_skill.name, True, settings.WHITE)
            surface.blit(name, (detail_rect.x + 24, detail_rect.y + 18))
            desc = self.wrap_description(self.selected_skill.description)
            for i, line in enumerate(desc):
                surf = self.small_font.render(line, True, settings.LIGHT_GREY)
                surface.blit(surf, (detail_rect.x + 24, detail_rect.y + 90 + i * 26))
            mod_lines = [f"{key}: {value}" for key, value in self.selected_skill.modifiers.items()]
            for i, mod in enumerate(mod_lines):
                surf = self.small_font.render(mod, True, settings.ACCENT)
                surface.blit(surf, (detail_rect.x + 24, detail_rect.y + 220 + i * 28))

    def wrap_description(self, text: str) -> List[str]:
        words = text.split()
        lines: List[str] = []
        current: List[str] = []
        while words:
            current.append(words.pop(0))
            if self.small_font.size(" ".join(current))[0] > 480:
                current.pop()
                lines.append(" ".join(current))
                current = []
        if current:
            lines.append(" ".join(current))
        return lines
