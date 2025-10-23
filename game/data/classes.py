from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Ability:
    name: str
    description: str
    cost: int
    cooldown: int
    effect: Dict[str, int]


@dataclass
class Archetype:
    name: str
    role: str
    strengths: List[str]
    weaknesses: List[str]
    traits: List[str]
    stat_block: Dict[str, int]
    abilities: List[Ability] = field(default_factory=list)
    signature_skill: str = ""


BASE_ARCHETYPES: Dict[str, Archetype] = {
    "Vanguard": Archetype(
        name="Vanguard",
        role="Defender",
        strengths=["High armor", "Area control", "Taunt"],
        weaknesses=["Limited ranged options"],
        traits=["Guardian's Oath", "Shield Wall"],
        stat_block={"hp": 120, "mana": 60, "strength": 14, "agility": 8, "focus": 10},
        abilities=[
            Ability(
                name="Shield Slam",
                description="Stun a nearby enemy and generate threat.",
                cost=15,
                cooldown=2,
                effect={"stun": 1, "threat": 20},
            ),
            Ability(
                name="Bulwark",
                description="Raise a barrier that reduces incoming damage for the party.",
                cost=20,
                cooldown=4,
                effect={"damage_reduction": 25, "duration": 2},
            ),
        ],
        signature_skill="Unbreakable Bastion",
    ),
    "Mistweaver": Archetype(
        name="Mistweaver",
        role="Support",
        strengths=["Versatile healing", "Illusory decoys", "Crowd control"],
        weaknesses=["Fragile", "Requires careful positioning"],
        traits=["Ethereal Step", "Mystic Harmonies"],
        stat_block={"hp": 80, "mana": 140, "strength": 6, "agility": 12, "focus": 18},
        abilities=[
            Ability(
                name="Healing Vapors",
                description="Soothing mist heals allies in a cone.",
                cost=20,
                cooldown=2,
                effect={"heal": 30, "targets": 3},
            ),
            Ability(
                name="Dreambind",
                description="Tangle foes with spectral chains, slowing them.",
                cost=18,
                cooldown=3,
                effect={"slow": 45, "duration": 3},
            ),
        ],
        signature_skill="Veil of Serenity",
    ),
    "Riftblade": Archetype(
        name="Riftblade",
        role="Striker",
        strengths=["Blink mobility", "Critical bursts", "Elemental finishers"],
        weaknesses=["Reliant on combo points"],
        traits=["Phase Dancer", "Arc Surge"],
        stat_block={"hp": 90, "mana": 80, "strength": 16, "agility": 14, "focus": 8},
        abilities=[
            Ability(
                name="Rift Strike",
                description="Dash through enemies leaving a crackling rift.",
                cost=10,
                cooldown=1,
                effect={"damage": 35, "combo": 1},
            ),
            Ability(
                name="Anomaly Collapse",
                description="Detonate all rifts for heavy damage.",
                cost=25,
                cooldown=4,
                effect={"damage": 80, "aoe": True},
            ),
        ],
        signature_skill="Event Horizon",
    ),
    "Skysage": Archetype(
        name="Skysage",
        role="Controller",
        strengths=["Battlefield vision", "Storm magic", "Summons"],
        weaknesses=["Lower physical defense"],
        traits=["Eye of the Tempest", "Stormcaller"],
        stat_block={"hp": 85, "mana": 130, "strength": 7, "agility": 11, "focus": 20},
        abilities=[
            Ability(
                name="Chain Tempest",
                description="Arc lightning between clustered foes.",
                cost=22,
                cooldown=3,
                effect={"damage": 28, "jumps": 4},
            ),
            Ability(
                name="Windward Aegis",
                description="Summon a cyclone that deflects projectiles.",
                cost=25,
                cooldown=5,
                effect={"projectile_block": True, "duration": 4},
            ),
        ],
        signature_skill="Celestial Convergence",
    ),
}
