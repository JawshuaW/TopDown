from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

from game.core.entities import Enemy, PlayerCharacter


@dataclass
class CombatLogEntry:
    actor: str
    action: str
    value: int | None = None

    def format(self) -> str:
        if self.value is None:
            return f"{self.actor} {self.action}"
        return f"{self.actor} {self.action} ({self.value})"


class CombatSimulator:
    def __init__(self, party: List[PlayerCharacter], enemies: List[Enemy]) -> None:
        self.party = party
        self.enemies = enemies
        self.log: List[CombatLogEntry] = []
        self.defeated: List[Enemy] = []

    def run_round(self) -> None:
        for hero in list(self.party):
            if not self.enemies:
                break
            target = random.choice(self.enemies)
            dmg = max(0, hero.stats.get("strength", 8) + random.randint(-2, 5))
            target.hp -= dmg
            self.log.append(CombatLogEntry(hero.codename, "strikes", dmg))
            if not target.is_alive():
                self.log.append(CombatLogEntry(target.name, "is defeated"))
                self.enemies.remove(target)
                self.defeated.append(target)
        for enemy in list(self.enemies):
            if not self.party:
                break
            target = random.choice(self.party)
            dmg = max(0, enemy.strength + random.randint(-3, 4))
            target.stats["hp"] = max(0, target.stats.get("hp", target.max_hp) - dmg)
            self.log.append(CombatLogEntry(enemy.name, f"hits {target.codename}", dmg))
            if target.stats.get("hp", 0) <= 0:
                self.log.append(CombatLogEntry(target.codename, "falls in battle"))
                self.party.remove(target)

    def victory(self) -> bool:
        return not self.enemies

    def defeat(self) -> bool:
        return not self.party
