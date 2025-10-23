from __future__ import annotations

import pygame

from game import settings
from game.core.entities import generate_party
from game.core.inventory import Inventory
from game.data.quests import QUESTS
from game.state_machine import GameState
from game.states.base import BaseMenuState, MenuOption


class MainMenuState(BaseMenuState, GameState):
    def __init__(self, app: "GameApp") -> None:
        GameState.__init__(self, app)
        BaseMenuState.__init__(self, app)
        self.title = "Exiles of Aether"
        self.subtitle = "Top-down rogue-lite expedition into the Shattered Vaults"
        self.background = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.background.fill((14, 20, 30))
        self._init_options()

    def _init_options(self) -> None:
        self.options = [
            MenuOption(
                "Begin Expedition",
                self.start_new_game,
                "Forge a new squad of three exiles and descend into procedural vaults.",
            ),
            MenuOption(
                "Party Configurator",
                lambda: self.app.state_machine.switch("party"),
                "Curate your current party composition, adjust formation, and inspect synergies.",
            ),
            MenuOption(
                "Skill Laboratory",
                lambda: self.app.state_machine.switch("skills_editor"),
                "Unlock, respec, and tune advanced combat techniques for your roster.",
            ),
            MenuOption(
                "Codex & Lore",
                self.view_codex,
                "Review discovered quests, factions, and world lore entries unlocked during runs.",
            ),
            MenuOption("Exit", self.quit_game),
        ]

    def start_new_game(self) -> None:
        if not self.app.player_party:
            self.app.player_party = generate_party()
            inventory = Inventory()
            inventory.gold = self.app.gold
            inventory.add_item("Wayfarer Rations", 3)
            self.app.inventory = inventory.items
        self.app.state_machine.switch("world", new_run=True)

    def view_codex(self) -> None:
        lines = []
        for quest in QUESTS.values():
            lines.append(f"{quest.name}: {quest.summary}")
        print("\n".join(lines))

    def quit_game(self) -> None:
        self.app.running = False

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))
        super().draw(surface)
