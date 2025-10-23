from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class LootTable:
    gold_range: range
    items: Dict[str, float]


@dataclass
class EnemyTemplate:
    name: str
    rank: str
    hp: int
    mana: int
    strength: int
    agility: int
    focus: int
    abilities: List[str]
    traits: List[str]
    loot: LootTable


ENEMIES: Dict[str, EnemyTemplate] = {
    "Ash Wraith": EnemyTemplate(
        name="Ash Wraith",
        rank="Elite",
        hp=150,
        mana=90,
        strength=18,
        agility=16,
        focus=14,
        abilities=["Cinder Lash", "Soul Siphon", "Immolate"],
        traits=["Phasing", "Burning Aura"],
        loot=LootTable(gold_range=range(30, 60), items={"Mistweave Ampoule": 0.15}),
    ),
    "Vault Sentry": EnemyTemplate(
        name="Vault Sentry",
        rank="Guardian",
        hp=220,
        mana=40,
        strength=22,
        agility=8,
        focus=6,
        abilities=["Shock Baton", "Suppressive Field"],
        traits=["Fortified", "Sentinel Network"],
        loot=LootTable(gold_range=range(18, 40), items={"Guardian Bulwark": 0.05}),
    ),
    "Hollow Corsair": EnemyTemplate(
        name="Hollow Corsair",
        rank="Skirmisher",
        hp=110,
        mana=50,
        strength=14,
        agility=20,
        focus=10,
        abilities=["Spectral Volley", "Blink Pirouette"],
        traits=["Evasive", "Arc Infusion"],
        loot=LootTable(gold_range=range(12, 28), items={"Iron Sabre": 0.12}),
    ),
}
