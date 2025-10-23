from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Item:
    name: str
    category: str
    description: str
    value: int
    stats: Dict[str, int]
    rarity: str = "Common"


ITEMS: Dict[str, Item] = {
    "Iron Sabre": Item(
        name="Iron Sabre",
        category="Weapon",
        description="Reliable blade favored by Riftblades learning to phase-step.",
        value=45,
        stats={"strength": 2, "agility": 1},
        rarity="Uncommon",
    ),
    "Guardian Bulwark": Item(
        name="Guardian Bulwark",
        category="Shield",
        description="Vanguard ceremonial shield etched with oath sigils.",
        value=80,
        stats={"hp": 15, "armor": 4},
        rarity="Rare",
    ),
    "Mistweave Ampoule": Item(
        name="Mistweave Ampoule",
        category="Potion",
        description="Condensed healing vapors to restore party vitality.",
        value=60,
        stats={"heal": 60},
        rarity="Rare",
    ),
    "Stormglass Focus": Item(
        name="Stormglass Focus",
        category="Accessory",
        description="A resonant crystal that amplifies Skysage channeling.",
        value=120,
        stats={"focus": 4, "mana": 25},
        rarity="Epic",
    ),
    "Wayfarer Rations": Item(
        name="Wayfarer Rations",
        category="Consumable",
        description="Restores stamina and removes exhaustion stacks.",
        value=18,
        stats={"exhaustion": -1},
    ),
}


SHOP_STOCK = {
    "Arsenal": ["Iron Sabre", "Guardian Bulwark"],
    "Apothecary": ["Mistweave Ampoule", "Wayfarer Rations"],
    "Arcana": ["Stormglass Focus", "Mistweave Ampoule"],
}
