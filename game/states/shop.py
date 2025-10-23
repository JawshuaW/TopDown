from __future__ import annotations

import pygame

from game import settings
from game.data.items import ITEMS, SHOP_STOCK
from game.state_machine import GameState


class ShopState(GameState):
    def __init__(self, app: "GameApp") -> None:
        super().__init__(app)
        self.font = pygame.font.Font(settings.FONT_PATH, 26)
        self.small_font = pygame.font.Font(settings.FONT_PATH, 20)
        self.stalls = list(SHOP_STOCK.keys())
        self.index = 0
        self.message = ""

    def enter(self, **params) -> None:
        self.message = ""

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.state_machine.switch("pause")
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.index = (self.index - 1) % len(self.stalls)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.index = (self.index + 1) % len(self.stalls)
            elif event.key == pygame.K_RETURN:
                self.buy_first_item()
            elif event.key == pygame.K_s:
                self.sell_first_item()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((12, 18, 24))
        title = self.font.render("Vault Caravan", True, settings.WHITE)
        surface.blit(title, (80, 50))
        gold_text = self.small_font.render(f"Gold: {self.app.gold}", True, settings.ACCENT)
        surface.blit(gold_text, (80, 100))
        for i, stall in enumerate(self.stalls):
            rect = pygame.Rect(80 + i * 360, 160, 320, 420)
            pygame.draw.rect(surface, (24, 28, 36), rect, border_radius=10)
            border = settings.ACCENT if i == self.index else settings.LIGHT_GREY
            pygame.draw.rect(surface, border, rect, 2)
            stall_text = self.font.render(stall, True, settings.WHITE)
            surface.blit(stall_text, (rect.x + 18, rect.y + 18))
            for j, item_name in enumerate(SHOP_STOCK[stall]):
                item = ITEMS[item_name]
                y = rect.y + 80 + j * 110
                item_rect = pygame.Rect(rect.x + 12, y, rect.width - 24, 100)
                pygame.draw.rect(surface, (30, 36, 46), item_rect, border_radius=8)
                pygame.draw.rect(surface, settings.LIGHT_GREY, item_rect, 1)
                name = self.small_font.render(item.name, True, settings.WHITE)
                surface.blit(name, (item_rect.x + 12, item_rect.y + 10))
                desc = self.small_font.render(item.description[:30] + "...", True, settings.LIGHT_GREY)
                surface.blit(desc, (item_rect.x + 12, item_rect.y + 40))
                price = self.small_font.render(f"{item.value}g", True, settings.ACCENT)
                surface.blit(price, (item_rect.x + 12, item_rect.y + 70))
        hint = "ENTER buy | S sell first owned item"
        hint_surf = self.small_font.render(hint, True, settings.LIGHT_GREY)
        surface.blit(hint_surf, (80, 620))
        if self.message:
            msg = self.small_font.render(self.message, True, settings.WHITE)
            surface.blit(msg, (80, 650))

    def buy_first_item(self) -> None:
        stall = self.stalls[self.index]
        if not SHOP_STOCK[stall]:
            self.message = "Sold out!"
            return
        item_name = SHOP_STOCK[stall][0]
        cost = ITEMS[item_name].value
        if self.app.gold < cost:
            self.message = "Insufficient gold"
            return
        self.app.gold -= cost
        self.app.inventory[item_name] = self.app.inventory.get(item_name, 0) + 1
        self.message = f"Purchased {item_name}"

    def sell_first_item(self) -> None:
        if not self.app.inventory:
            self.message = "Nothing to sell"
            return
        item_name, count = next(iter(self.app.inventory.items()))
        payout = int(ITEMS[item_name].value * 0.6)
        self.app.gold += payout
        if count <= 1:
            del self.app.inventory[item_name]
        else:
            self.app.inventory[item_name] = count - 1
        self.message = f"Sold {item_name} for {payout}g"
