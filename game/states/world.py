from __future__ import annotations

import random
from typing import List

import pygame

from game import settings
from game.core.combat import CombatSimulator
from game.core.entities import instantiate_enemy
from game.data.enemies import ENEMIES
from game.core.world import TILE_FLOOR, generate_dungeon
from game.state_machine import GameState
from game.ui.components import GridRenderer


class WorldState(GameState):
    def __init__(self, app: "GameApp") -> None:
        super().__init__(app)
        self.grid: List[List[int]] = []
        self.rooms = []
        self.renderer = GridRenderer(tile_size=48)
        self.camera = pygame.Rect(0, 0, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        self.player_pos = pygame.Vector2(3, 3)
        self.party_health: List[int] = []
        self.toast_timer = 0.0
        self.toast_text = ""
        self.font = pygame.font.Font(settings.FONT_PATH, 24)
        self.log: List[str] = []

    def enter(self, **params) -> None:
        new_run = params.get("new_run", False)
        if new_run or not self.grid:
            self.grid, self.rooms = generate_dungeon()
            self.player_pos.update(3, 3)
            self.toast("Entering the Shattered Vaults")
            self.party_health = [member.max_hp for member in self.app.player_party]
        if params.get("combat_log"):
            self.log = params["combat_log"]

    def toast(self, text: str, duration: float = 2.5) -> None:
        self.toast_text = text
        self.toast_timer = duration

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.state_machine.switch("pause")
            elif event.key == pygame.K_SPACE:
                self.initiate_combat()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.initiate_combat()

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x += 1
        if move.length_squared() > 0:
            move = move.normalize()
            new_pos = self.player_pos + move * dt * 4
            if self.is_walkable(new_pos):
                self.player_pos = new_pos
        self.center_camera_on_player()
        if self.toast_timer > 0:
            self.toast_timer -= dt

    def draw(self, surface: pygame.Surface) -> None:
        dungeon_surface = pygame.Surface(
            (len(self.grid[0]) * self.renderer.tile_size, len(self.grid) * self.renderer.tile_size)
        )
        self.renderer.draw(dungeon_surface, self.grid)
        player_rect = pygame.Rect(
            int(self.player_pos.x * self.renderer.tile_size),
            int(self.player_pos.y * self.renderer.tile_size),
            self.renderer.tile_size,
            self.renderer.tile_size,
        )
        pygame.draw.rect(dungeon_surface, (220, 180, 70), player_rect.inflate(-16, -16), border_radius=8)
        surface.blit(dungeon_surface, (0, 0), self.camera)

        if self.toast_timer > 0:
            text = self.font.render(self.toast_text, True, settings.WHITE)
            surface.blit(text, (20, 20))
        if self.log:
            self.draw_log(surface)

    def draw_log(self, surface: pygame.Surface) -> None:
        base_y = settings.WINDOW_HEIGHT - 160
        log_rect = pygame.Rect(20, base_y - 10, 420, 140)
        pygame.draw.rect(surface, (18, 20, 26), log_rect)
        pygame.draw.rect(surface, settings.ACCENT, log_rect, 2)
        for i, line in enumerate(self.log[-5:]):
            text = self.font.render(line, True, settings.LIGHT_GREY)
            surface.blit(text, (log_rect.x + 12, log_rect.y + 12 + i * 24))

    def center_camera_on_player(self) -> None:
        px = int(self.player_pos.x * self.renderer.tile_size)
        py = int(self.player_pos.y * self.renderer.tile_size)
        self.camera.center = (px, py)
        world_w = len(self.grid[0]) * self.renderer.tile_size
        world_h = len(self.grid) * self.renderer.tile_size
        self.camera.clamp_ip(pygame.Rect(0, 0, world_w, world_h))

    def is_walkable(self, pos: pygame.Vector2) -> bool:
        x = int(pos.x)
        y = int(pos.y)
        if y < 0 or y >= len(self.grid) or x < 0 or x >= len(self.grid[0]):
            return False
        return self.grid[y][x] == TILE_FLOOR

    def initiate_combat(self) -> None:
        if not self.app.player_party:
            self.toast("No party configured!", 2.0)
            return
        templates = ["Ash Wraith", "Vault Sentry", "Hollow Corsair"]
        encounter = [instantiate_enemy(random.choice(templates)) for _ in range(random.randint(1, 3))]
        simulator = CombatSimulator(list(self.app.player_party), encounter)
        simulator.run_round()
        log = [entry.format() for entry in simulator.log]
        if simulator.victory():
            self.toast("Encounter cleared!", 2.0)
        elif simulator.defeat():
            self.toast("Squad routed!", 2.0)
        if simulator.defeated:
            loot = sum(enemy.gold_reward for enemy in simulator.defeated)
            self.app.gold += loot
            log.append(f"Loot recovered: {loot} gold")
            for enemy in simulator.defeated:
                template = ENEMIES.get(enemy.name)
                if not template:
                    continue
                for item_name, chance in template.loot.items.items():
                    if random.random() <= chance:
                        self.app.inventory[item_name] = self.app.inventory.get(item_name, 0) + 1
                        log.append(f"Salvaged {item_name}")
        self.log = log
