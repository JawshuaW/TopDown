from __future__ import annotations

import pygame

from game import settings
from game.state_machine import GameState
from game.states.base import BaseMenuState, MenuOption


class PauseMenuState(BaseMenuState, GameState):
    def __init__(self, app: "GameApp") -> None:
        GameState.__init__(self, app)
        BaseMenuState.__init__(self, app)
        self.title = "Expedition Paused"
        self.subtitle = "Manage your squad mid-run"
        self.overlay = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 160))
        self.options = [
            MenuOption(
                "Resume",
                lambda: self.app.state_machine.switch("world"),
            ),
            MenuOption(
                "Squad Loadout",
                lambda: self.app.state_machine.switch("player_editor"),
                "Review party equipment, swap weapons, and assign relics.",
            ),
            MenuOption(
                "Visit Merchant",
                lambda: self.app.state_machine.switch("shop"),
                "Trade relics and salvage with the traveling merchant caravan.",
            ),
            MenuOption(
                "Return to Title",
                self.back_to_menu,
                "Abandon the current delve and return to the citadel concourse.",
            ),
        ]

    def back_to_menu(self) -> None:
        self.app.state_machine.switch("menu")

    def draw(self, surface: pygame.Surface) -> None:
        self.app.state_machine.states["world"].draw(surface)
        surface.blit(self.overlay, (0, 0))
        super().draw(surface)
