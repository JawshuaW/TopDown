from __future__ import annotations

import pygame

from game import settings
from game.data.items import ITEMS
from game.state_machine import GameState


class PlayerEditorState(GameState):
    def __init__(self, app: "GameApp") -> None:
        super().__init__(app)
        self.font = pygame.font.Font(settings.FONT_PATH, 26)
        self.small_font = pygame.font.Font(settings.FONT_PATH, 20)
        self.index = 0
        self.selected_slot = "Weapon"
        self.slots = ["Weapon", "Shield", "Accessory"]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.state_machine.switch("pause")
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.index = (self.index - 1) % len(self.app.player_party)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.index = (self.index + 1) % len(self.app.player_party)
            elif event.key in (pygame.K_UP, pygame.K_w):
                slot_index = (self.slots.index(self.selected_slot) - 1) % len(self.slots)
                self.selected_slot = self.slots[slot_index]
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                slot_index = (self.slots.index(self.selected_slot) + 1) % len(self.slots)
                self.selected_slot = self.slots[slot_index]
            elif event.key == pygame.K_RETURN:
                self.cycle_equipment()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((16, 20, 28))
        if not self.app.player_party:
            text = self.font.render("No party members configured", True, settings.ERROR)
            surface.blit(text, text.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)))
            return
        member = self.app.player_party[self.index]
        title = self.font.render(f"{member.codename} - {member.archetype.name}", True, settings.WHITE)
        surface.blit(title, (80, 60))
        stats = [f"HP {member.max_hp}", f"Mana {member.max_mana}"] + [
            f"{key.title()}: {value}" for key, value in member.stats.items() if key not in {"hp", "mana"}
        ]
        for i, stat in enumerate(stats):
            surf = self.small_font.render(stat, True, settings.LIGHT_GREY)
            surface.blit(surf, (80, 120 + i * 28))

        for i, slot in enumerate(self.slots):
            rect = pygame.Rect(80, 260 + i * 100, 420, 80)
            pygame.draw.rect(surface, (24, 30, 40), rect, border_radius=8)
            border_color = settings.ACCENT if slot == self.selected_slot else settings.LIGHT_GREY
            pygame.draw.rect(surface, border_color, rect, 2)
            equipped = member.equipped.get(slot.lower(), "Empty")
            surf = self.small_font.render(f"{slot}: {equipped}", True, settings.WHITE)
            surface.blit(surf, (rect.x + 16, rect.y + 24))

    def cycle_equipment(self) -> None:
        if not self.app.player_party:
            return
        member = self.app.player_party[self.index]
        candidates = [item for item in ITEMS if item not in member.equipped.values()]
        if not candidates:
            return
        selection = candidates[0]
        member.equipped[self.selected_slot.lower()] = selection
        member.recalculate_stats()
