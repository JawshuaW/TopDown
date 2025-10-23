from __future__ import annotations

import os
import pathlib
from typing import Dict, List

import pygame

from game import settings
from game.state_machine import StateMachine
from game.states.main_menu import MainMenuState
from game.states.world import WorldState
from game.states.pause_menu import PauseMenuState
from game.states.skills_editor import SkillsEditorState
from game.states.player_editor import PlayerEditorState
from game.states.shop import ShopState
from game.states.party import PartyManagementState


class GameApp:
    """High level application object that holds shared state."""

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(settings.TITLE)

        self.running = False
        self.state_machine = StateMachine(self)
        self.assets: Dict[str, pygame.Surface] = {}
        self.player_party: List[dict] = []
        self.inventory: Dict[str, int] = {}
        self.gold = 120
        self.unlocked_skills: Dict[str, List[str]] = {}

        self._ensure_directories()
        self._register_states()

    def _ensure_directories(self) -> None:
        pathlib.Path(settings.SAVE_DIR).mkdir(parents=True, exist_ok=True)
        pathlib.Path(settings.ASSET_DIR).mkdir(parents=True, exist_ok=True)

    def _register_states(self) -> None:
        self.state_machine.register("menu", MainMenuState)
        self.state_machine.register("world", WorldState)
        self.state_machine.register("pause", PauseMenuState)
        self.state_machine.register("skills_editor", SkillsEditorState)
        self.state_machine.register("player_editor", PlayerEditorState)
        self.state_machine.register("shop", ShopState)
        self.state_machine.register("party", PartyManagementState)

    def run(self) -> None:
        self.running = True
        self.state_machine.switch("menu")
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.state_machine.handle_event(event)

            self.state_machine.update(dt)
            self.state_machine.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    os.environ.setdefault("SDL_VIDEO_CENTERED", "1")
    GameApp().run()
