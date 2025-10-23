from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List

from game.data.classes import Archetype, BASE_ARCHETYPES
from game.data.items import ITEMS


@dataclass
class Skill:
    name: str
    description: str
    tier: int
    modifiers: Dict[str, int]


@dataclass
class PlayerCharacter:
    codename: str
    archetype: Archetype
    level: int = 1
    xp: int = 0
    base_stats: Dict[str, int] = field(default_factory=dict)
    stats: Dict[str, int] = field(default_factory=dict)
    equipped: Dict[str, str] = field(default_factory=dict)
    learned_skills: List[Skill] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.base_stats:
            self.base_stats = dict(self.archetype.stat_block)
        self.recalculate_stats()

    @property
    def max_hp(self) -> int:
        return self.stats.get("hp", 100) + self.level * 5

    @property
    def max_mana(self) -> int:
        return self.stats.get("mana", 60) + self.level * 4

    def recalculate_stats(self) -> None:
        self.stats = dict(self.base_stats)
        for item_name in self.equipped.values():
            if not item_name:
                continue
            for key, value in ITEMS[item_name].stats.items():
                self.stats[key] = self.stats.get(key, 0) + value

    def summary(self) -> str:
        return (
            f"{self.codename} - {self.archetype.name} Lv.{self.level}"
            f" | STR {self.stats.get('strength', 0)}"
            f" | AGI {self.stats.get('agility', 0)}"
            f" | FOC {self.stats.get('focus', 0)}"
        )


def generate_party(seed: int | None = None) -> List[PlayerCharacter]:
    rng = random.Random(seed)
    archetypes = list(BASE_ARCHETYPES.values())
    rng.shuffle(archetypes)
    party: List[PlayerCharacter] = []
    for archetype in archetypes[:3]:
        codename = f"{archetype.name}-{rng.randint(100, 999)}"
        party.append(PlayerCharacter(codename=codename, archetype=archetype))
    return party


def skill_catalogue() -> List[Skill]:
    return [
        Skill(
            name="Chrono Anchor",
            description="Bookmark an ally's timeline to undo fatal damage once.",
            tier=3,
            modifiers={"revive": 1, "cooldown": 6},
        ),
        Skill(
            name="Aether Torrent",
            description="Unleash concentrated aether for devastating single-target damage.",
            tier=2,
            modifiers={"damage": 120, "mana_cost": 35},
        ),
        Skill(
            name="Echo Step",
            description="Leave an illusionary clone that taunts enemies for one round.",
            tier=1,
            modifiers={"taunt": 1, "duration": 1},
        ),
    ]


@dataclass
class Enemy:
    name: str
    hp: int
    mana: int
    strength: int
    agility: int
    focus: int
    xp_reward: int
    gold_reward: int

    def is_alive(self) -> bool:
        return self.hp > 0


def instantiate_enemy(template_name: str) -> Enemy:
    from game.data.enemies import ENEMIES

    template = ENEMIES[template_name]
    hp = template.hp
    gold = random.randint(template.loot.gold_range.start, template.loot.gold_range.stop)
    xp = int((template.hp + template.strength * 4 + template.focus * 3) / 4)
    return Enemy(
        name=template.name,
        hp=hp,
        mana=template.mana,
        strength=template.strength,
        agility=template.agility,
        focus=template.focus,
        xp_reward=xp,
        gold_reward=gold,
    )
