from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import pygame

from game import settings
from game.state_machine import GameState


@dataclass
class Job:
    name: str
    summary: str
    money: int
    rep: int
    heat: int


@dataclass
class Upgrade:
    key: str
    name: str
    summary: str
    base_cost: int
    level: int = 0
    max_level: int = 5

    def cost(self) -> int:
        return int(self.base_cost * (1.4**self.level))


class UnderbossState(GameState):
    def __init__(self, app: "GameApp") -> None:
        super().__init__(app)
        self.title_font = pygame.font.Font(settings.FONT_PATH, 42)
        self.subtitle_font = pygame.font.Font(settings.FONT_PATH, 22)
        self.font = pygame.font.Font(settings.FONT_PATH, 24)
        self.small_font = pygame.font.Font(settings.FONT_PATH, 18)
        self.tiny_font = pygame.font.Font(settings.FONT_PATH, 16)

        self.tabs = ["Jobs", "Imperium", "Stats"]
        self.active_tab = "Jobs"
        self.tab_rects: Dict[str, pygame.Rect] = {}

        self.job_categories = ["Street Hustles", "Black Market", "Nightlife", "High Stakes"]
        self.active_job_category = self.job_categories[0]
        self.category_rects: Dict[str, pygame.Rect] = {}
        self.job_rects: List[Tuple[pygame.Rect, Job]] = []

        self.imperium_tabs = [
            "Training",
            "Hideout",
            "Crew",
            "Weapons",
            "Heat Control",
            "Market",
        ]
        self.active_imperium_tab = self.imperium_tabs[0]
        self.imperium_rects: Dict[str, pygame.Rect] = {}
        self.upgrade_rects: List[Tuple[pygame.Rect, Upgrade]] = []

        self.money = 5200
        self.rep = 18
        self.heat = 4
        self.influence = 6
        self.power = 8
        self.respect = 10

        self.skills = {
            "strength": 1,
            "hustle": 1,
            "power": 1,
            "heat": 1,
            "stealth": 1,
            "intelligence": 1,
            "rep": 1,
        }

        self.hideout_level = 1
        self.bodyguards = [
            {"name": "Vera Steel", "role": "Shieldbearer", "level": 2},
            {"name": "Kade Flint", "role": "Sniper", "level": 1},
            {"name": "Mira Ghost", "role": "Scout", "level": 1},
        ]

        self.jobs = {
            "Street Hustles": [
                Job(
                    "Corner Collections",
                    "Lean on street debtors and keep the cashflow steady.",
                    180,
                    2,
                    1,
                ),
                Job(
                    "Chop-Shop Run",
                    "Strip boosted rides and move the parts through fences.",
                    260,
                    3,
                    2,
                ),
                Job(
                    "Union Pressure",
                    "Squeeze a local union for protection fees and favors.",
                    340,
                    4,
                    3,
                ),
            ],
            "Black Market": [
                Job(
                    "Smuggled Medicine",
                    "Move contraband supplies through a pop-up clinic.",
                    420,
                    4,
                    3,
                ),
                Job(
                    "Encrypted Drop",
                    "Exchange phantom data caches on a ghost network.",
                    520,
                    5,
                    4,
                ),
                Job(
                    "Luxury Relay",
                    "Broker rare artifacts to collectors with deep pockets.",
                    640,
                    6,
                    5,
                ),
            ],
            "Nightlife": [
                Job(
                    "Club Takeover",
                    "Run the door and skim revenue from a packed venue.",
                    360,
                    3,
                    2,
                ),
                Job(
                    "VIP Escort",
                    "Guarantee safety for a celebrity in exchange for favors.",
                    480,
                    4,
                    3,
                ),
                Job(
                    "Backroom Auctions",
                    "Host underground auctions with bidders you can leverage.",
                    620,
                    5,
                    4,
                ),
            ],
            "High Stakes": [
                Job(
                    "Data Fortress Raid",
                    "Breach a corporate vault and extract payout chips.",
                    950,
                    7,
                    7,
                ),
                Job(
                    "Convoy Ambush",
                    "Intercept an armored convoy and vanish without a trace.",
                    1120,
                    8,
                    8,
                ),
                Job(
                    "Syndicate Summit",
                    "Negotiate a hostile takeover with leverage and muscle.",
                    1280,
                    9,
                    9,
                ),
            ],
        }

        self.training_upgrades = [
            Upgrade(
                "strength",
                "Strength Conditioning",
                "Toughen up the crew for higher combat output.",
                420,
            ),
            Upgrade(
                "hustle",
                "Hustle Finance",
                "Increase money gained from every job.",
                450,
            ),
            Upgrade(
                "power",
                "Power Projection",
                "Boost intimidation to win negotiations.",
                480,
            ),
            Upgrade(
                "heat",
                "Heat Management",
                "Reduce heat gained per operation.",
                460,
            ),
            Upgrade(
                "stealth",
                "Shadowcraft",
                "Improve stealth for cleaner getaways.",
                520,
            ),
            Upgrade(
                "intelligence",
                "Cipher Mind",
                "Crack intel faster for sharper payouts.",
                500,
            ),
            Upgrade(
                "rep",
                "Reputation Craft",
                "Amplify reputation growth from jobs.",
                540,
            ),
        ]

        self.hideout_upgrades = [
            Upgrade(
                "safehouse",
                "Safehouse Network",
                "Boost job earnings with better staging points.",
                600,
            ),
            Upgrade(
                "workshop",
                "Custom Workshop",
                "Improve weapon effectiveness for field crews.",
                680,
            ),
            Upgrade(
                "surveillance",
                "Surveillance Hub",
                "Reveal heat spikes and soften exposure.",
                640,
            ),
            Upgrade(
                "vault",
                "Vault Expansion",
                "Store more resources for long-term gains.",
                720,
            ),
        ]

        self.crew_upgrades = [
            Upgrade(
                "enforcers",
                "Enforcer Roster",
                "Increase combat power and job success.",
                560,
            ),
            Upgrade(
                "fixers",
                "Fixer Network",
                "Reduce heat and smooth negotiations.",
                520,
            ),
            Upgrade(
                "scouts",
                "Scout Wing",
                "Improve stealth and intel for operations.",
                540,
            ),
            Upgrade(
                "medics",
                "Street Medics",
                "Keep bodyguards operational after missions.",
                500,
            ),
        ]

        self.weapon_upgrades = [
            Upgrade(
                "sidearms",
                "Custom Sidearms",
                "Reliable firepower for every squad.",
                620,
            ),
            Upgrade(
                "rifles",
                "Long Rifle Cache",
                "Extend your reach and precision.",
                680,
            ),
            Upgrade(
                "heavy",
                "Heavy Gear",
                "Bring overwhelming force to key hits.",
                760,
            ),
            Upgrade(
                "armor",
                "Reactive Armor",
                "Increase survivability for the crew.",
                740,
            ),
        ]

        self.heat_control_upgrades = [
            Upgrade(
                "bribes",
                "Bribery Fund",
                "Smooth over incidents before they hit the news.",
                580,
            ),
            Upgrade(
                "lawyers",
                "Legal Shield",
                "Reduce penalties when heat is high.",
                620,
            ),
            Upgrade(
                "scrubbers",
                "Trace Scrubbers",
                "Erase digital trails after each job.",
                660,
            ),
        ]

        self.market_upgrades = [
            Upgrade(
                "routes",
                "Smuggler Routes",
                "Boost payout with optimized delivery paths.",
                600,
            ),
            Upgrade(
                "auctions",
                "Auction Access",
                "Sell premium goods for extra returns.",
                680,
            ),
            Upgrade(
                "fronts",
                "Front Companies",
                "Reduce heat and increase rep gains.",
                720,
            ),
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.state_machine.switch("menu")
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)

    def _handle_click(self, pos: Tuple[int, int]) -> None:
        for name, rect in self.tab_rects.items():
            if rect.collidepoint(pos):
                self.active_tab = name
                return

        if self.active_tab == "Jobs":
            for name, rect in self.category_rects.items():
                if rect.collidepoint(pos):
                    self.active_job_category = name
                    return
            for rect, job in self.job_rects:
                if rect.collidepoint(pos):
                    self._run_job(job)
                    return
        elif self.active_tab == "Imperium":
            for name, rect in self.imperium_rects.items():
                if rect.collidepoint(pos):
                    self.active_imperium_tab = name
                    return
            for rect, upgrade in self.upgrade_rects:
                if rect.collidepoint(pos):
                    self._purchase_upgrade(upgrade)
                    return

    def _run_job(self, job: Job) -> None:
        payout_multiplier = 1 + (self.skills["hustle"] * 0.05)
        hideout_bonus = 1 + (self.hideout_level - 1) * 0.04
        market_bonus = 1 + self._upgrade_level(self.market_upgrades) * 0.03
        money_gain = int(job.money * payout_multiplier * hideout_bonus * market_bonus)
        rep_gain = int(job.rep * (1 + self.skills["rep"] * 0.05))
        heat_delta = max(1, job.heat - int(self.skills["heat"] * 0.2))
        heat_delta = max(0, heat_delta - self._upgrade_level(self.heat_control_upgrades))
        self.money += money_gain
        self.rep += rep_gain
        self.heat = min(99, self.heat + heat_delta)
        self.influence += int(job.rep / 2)
        self.respect += int(job.money / 200)

    def _purchase_upgrade(self, upgrade: Upgrade) -> None:
        if upgrade.level >= upgrade.max_level:
            return
        cost = upgrade.cost()
        if self.money < cost:
            return
        self.money -= cost
        upgrade.level += 1
        if upgrade.key in self.skills:
            self.skills[upgrade.key] += 1
        if upgrade.key == "safehouse":
            self.hideout_level += 1
        if upgrade.key == "workshop":
            self.power += 1

    def _upgrade_level(self, upgrades: List[Upgrade]) -> int:
        return sum(upgrade.level for upgrade in upgrades)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((12, 16, 24))
        self._draw_header(surface)
        self._draw_tabs(surface)

        content_rect = pygame.Rect(40, 140, settings.WINDOW_WIDTH - 80, 540)
        pygame.draw.rect(surface, (18, 24, 34), content_rect, border_radius=14)
        pygame.draw.rect(surface, (60, 80, 110), content_rect, 2, border_radius=14)

        if self.active_tab == "Jobs":
            self._draw_jobs(surface, content_rect)
        elif self.active_tab == "Imperium":
            self._draw_imperium(surface, content_rect)
        elif self.active_tab == "Stats":
            self._draw_stats(surface, content_rect)

    def _draw_header(self, surface: pygame.Surface) -> None:
        title = self.title_font.render("Underboss Imperium", True, settings.WHITE)
        subtitle = self.subtitle_font.render(
            "Build your criminal empire, grow your crew, and dominate the city.",
            True,
            settings.LIGHT_GREY,
        )
        surface.blit(title, (40, 24))
        surface.blit(subtitle, (40, 72))

        info = [
            f"Cash: ${self.money:,}",
            f"Rep: {self.rep}",
            f"Heat: {self.heat}",
            f"Power: {self.power}",
            f"Influence: {self.influence}",
        ]
        for i, label in enumerate(info):
            text = self.small_font.render(label, True, (220, 230, 240))
            surface.blit(text, (820, 32 + i * 22))

    def _draw_tabs(self, surface: pygame.Surface) -> None:
        self.tab_rects.clear()
        start_x = 40
        for tab in self.tabs:
            rect = pygame.Rect(start_x, 108, 160, 32)
            self.tab_rects[tab] = rect
            is_active = tab == self.active_tab
            color = (80, 120, 160) if is_active else (40, 54, 70)
            pygame.draw.rect(surface, color, rect, border_radius=8)
            pygame.draw.rect(surface, (120, 160, 200), rect, 2, border_radius=8)
            label = self.small_font.render(tab, True, settings.WHITE)
            surface.blit(label, (rect.x + 16, rect.y + 6))
            start_x += 176

    def _draw_jobs(self, surface: pygame.Surface, content_rect: pygame.Rect) -> None:
        self.category_rects.clear()
        self.job_rects.clear()
        category_rect = pygame.Rect(content_rect.x + 20, content_rect.y + 20, 220, 500)
        pygame.draw.rect(surface, (22, 30, 44), category_rect, border_radius=12)
        pygame.draw.rect(surface, (52, 74, 104), category_rect, 2, border_radius=12)

        for i, category in enumerate(self.job_categories):
            rect = pygame.Rect(category_rect.x + 16, category_rect.y + 20 + i * 68, 188, 52)
            self.category_rects[category] = rect
            is_active = category == self.active_job_category
            color = (72, 110, 150) if is_active else (30, 42, 58)
            pygame.draw.rect(surface, color, rect, border_radius=10)
            pygame.draw.rect(surface, (90, 130, 170), rect, 2, border_radius=10)
            label = self.tiny_font.render(category, True, settings.WHITE)
            surface.blit(label, (rect.x + 12, rect.y + 16))

        jobs_rect = pygame.Rect(content_rect.x + 260, content_rect.y + 20, 960, 500)
        pygame.draw.rect(surface, (20, 28, 40), jobs_rect, border_radius=12)
        pygame.draw.rect(surface, (50, 70, 100), jobs_rect, 2, border_radius=12)

        header = self.font.render(self.active_job_category, True, settings.WHITE)
        surface.blit(header, (jobs_rect.x + 20, jobs_rect.y + 16))

        for i, job in enumerate(self.jobs[self.active_job_category]):
            rect = pygame.Rect(jobs_rect.x + 20, jobs_rect.y + 64 + i * 138, 920, 118)
            self.job_rects.append((rect, job))
            pygame.draw.rect(surface, (28, 36, 52), rect, border_radius=12)
            pygame.draw.rect(surface, (86, 120, 160), rect, 2, border_radius=12)
            name = self.font.render(job.name, True, settings.WHITE)
            surface.blit(name, (rect.x + 20, rect.y + 16))
            summary_lines = self._wrap_text(job.summary, self.small_font, rect.width - 240)
            for line_index, line in enumerate(summary_lines[:2]):
                summary = self.small_font.render(line, True, settings.LIGHT_GREY)
                surface.blit(summary, (rect.x + 20, rect.y + 50 + line_index * 22))
            rewards = [
                f"+${job.money}",
                f"+{job.rep} Rep",
                f"+{job.heat} Heat",
            ]
            for reward_index, reward in enumerate(rewards):
                reward_text = self.small_font.render(reward, True, (200, 220, 240))
                surface.blit(reward_text, (rect.x + 640, rect.y + 20 + reward_index * 26))

    def _draw_imperium(self, surface: pygame.Surface, content_rect: pygame.Rect) -> None:
        self.imperium_rects.clear()
        self.upgrade_rects.clear()

        tab_x = content_rect.x + 20
        for tab in self.imperium_tabs:
            rect = pygame.Rect(tab_x, content_rect.y + 16, 160, 30)
            self.imperium_rects[tab] = rect
            is_active = tab == self.active_imperium_tab
            color = (70, 110, 150) if is_active else (34, 48, 66)
            pygame.draw.rect(surface, color, rect, border_radius=8)
            pygame.draw.rect(surface, (110, 150, 190), rect, 2, border_radius=8)
            label = self.tiny_font.render(tab, True, settings.WHITE)
            surface.blit(label, (rect.x + 10, rect.y + 8))
            tab_x += 176

        upgrades = self._get_active_upgrades()
        base_y = content_rect.y + 70
        for i, upgrade in enumerate(upgrades):
            rect = pygame.Rect(content_rect.x + 20, base_y + i * 108, 1200, 96)
            self.upgrade_rects.append((rect, upgrade))
            pygame.draw.rect(surface, (26, 34, 48), rect, border_radius=12)
            pygame.draw.rect(surface, (90, 130, 170), rect, 2, border_radius=12)

            name = self.font.render(upgrade.name, True, settings.WHITE)
            surface.blit(name, (rect.x + 20, rect.y + 12))
            summary_lines = self._wrap_text(upgrade.summary, self.small_font, rect.width - 340)
            for line_index, line in enumerate(summary_lines[:2]):
                summary = self.small_font.render(line, True, settings.LIGHT_GREY)
                surface.blit(summary, (rect.x + 20, rect.y + 44 + line_index * 20))

            level_label = self.small_font.render(
                f"Level {upgrade.level}/{upgrade.max_level}",
                True,
                (210, 220, 240),
            )
            surface.blit(level_label, (rect.x + 820, rect.y + 18))

            cost_label = self.small_font.render(
                f"Cost: ${upgrade.cost():,}",
                True,
                (210, 220, 240),
            )
            surface.blit(cost_label, (rect.x + 820, rect.y + 48))

    def _draw_stats(self, surface: pygame.Surface, content_rect: pygame.Rect) -> None:
        stats_rect = pygame.Rect(content_rect.x + 20, content_rect.y + 20, 520, 500)
        pygame.draw.rect(surface, (22, 30, 44), stats_rect, border_radius=12)
        pygame.draw.rect(surface, (70, 100, 140), stats_rect, 2, border_radius=12)

        stat_lines = [
            "Empire Overview",
            f"Cash Holdings: ${self.money:,}",
            f"Reputation: {self.rep}",
            f"Heat Level: {self.heat}",
            f"Influence Score: {self.influence}",
            f"Power Rating: {self.power}",
            f"Respect: {self.respect}",
        ]
        for i, line in enumerate(stat_lines):
            label = self.small_font.render(
                line,
                True,
                settings.WHITE if i == 0 else settings.LIGHT_GREY,
            )
            surface.blit(label, (stats_rect.x + 20, stats_rect.y + 20 + i * 26))

        combat_rect = pygame.Rect(content_rect.x + 560, content_rect.y + 20, 680, 200)
        pygame.draw.rect(surface, (22, 30, 44), combat_rect, border_radius=12)
        pygame.draw.rect(surface, (70, 100, 140), combat_rect, 2, border_radius=12)
        surface.blit(
            self.small_font.render("Combat & Crew", True, settings.WHITE),
            (combat_rect.x + 20, combat_rect.y + 16),
        )
        combat_lines = [
            f"Strength: {self.skills['strength']}",
            f"Power Projection: {self.skills['power']}",
            f"Weapon Mastery: {self._upgrade_level(self.weapon_upgrades)}",
            f"Enforcer Roster: {self._upgrade_level(self.crew_upgrades)}",
        ]
        for i, line in enumerate(combat_lines):
            label = self.small_font.render(line, True, settings.LIGHT_GREY)
            surface.blit(label, (combat_rect.x + 20, combat_rect.y + 52 + i * 22))

        economy_rect = pygame.Rect(content_rect.x + 560, content_rect.y + 240, 680, 160)
        pygame.draw.rect(surface, (22, 30, 44), economy_rect, border_radius=12)
        pygame.draw.rect(surface, (70, 100, 140), economy_rect, 2, border_radius=12)
        surface.blit(
            self.small_font.render("Economy & Operations", True, settings.WHITE),
            (economy_rect.x + 20, economy_rect.y + 16),
        )
        economy_lines = [
            f"Hustle Bonus: +{self.skills['hustle'] * 5}%",
            f"Hideout Level: {self.hideout_level}",
            f"Market Uplift: +{self._upgrade_level(self.market_upgrades) * 3}%",
            f"Heat Control: -{self._upgrade_level(self.heat_control_upgrades)}",
        ]
        for i, line in enumerate(economy_lines):
            label = self.small_font.render(line, True, settings.LIGHT_GREY)
            surface.blit(label, (economy_rect.x + 20, economy_rect.y + 52 + i * 22))

        bodyguard_rect = pygame.Rect(content_rect.x + 560, content_rect.y + 420, 680, 100)
        pygame.draw.rect(surface, (22, 30, 44), bodyguard_rect, border_radius=12)
        pygame.draw.rect(surface, (70, 100, 140), bodyguard_rect, 2, border_radius=12)
        surface.blit(
            self.small_font.render("Bodyguards", True, settings.WHITE),
            (bodyguard_rect.x + 20, bodyguard_rect.y + 12),
        )
        for i, guard in enumerate(self.bodyguards):
            label = self.tiny_font.render(
                f"{guard['name']} • {guard['role']} • Lv {guard['level']}",
                True,
                settings.LIGHT_GREY,
            )
            surface.blit(label, (bodyguard_rect.x + 20, bodyguard_rect.y + 38 + i * 18))

    def _get_active_upgrades(self) -> List[Upgrade]:
        if self.active_imperium_tab == "Training":
            return self.training_upgrades
        if self.active_imperium_tab == "Hideout":
            return self.hideout_upgrades
        if self.active_imperium_tab == "Crew":
            return self.crew_upgrades
        if self.active_imperium_tab == "Weapons":
            return self.weapon_upgrades
        if self.active_imperium_tab == "Heat Control":
            return self.heat_control_upgrades
        if self.active_imperium_tab == "Market":
            return self.market_upgrades
        return []

    def _wrap_text(self, text: str, font: pygame.font.Font, width: int) -> List[str]:
        words = text.split()
        lines = []
        current = ""
        for word in words:
            test = f"{current} {word}".strip()
            if font.size(test)[0] <= width:
                current = test
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines
