from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class QuestObjective:
    description: str
    target: str
    quantity: int


@dataclass
class Quest:
    name: str
    giver: str
    summary: str
    objectives: List[QuestObjective]
    rewards: Dict[str, int]
    reputation: Dict[str, int]


QUESTS: Dict[str, Quest] = {
    "Echoes in the Vault": Quest(
        name="Echoes in the Vault",
        giver="Archivist Lyra",
        summary="Disrupt the Ash Wraith ritual siphoning power from the skyforge.",
        objectives=[
            QuestObjective(
                description="Locate the ritual chamber beneath the collapsed observatory.",
                target="Explore",
                quantity=1,
            ),
            QuestObjective(
                description="Defeat the Ash Wraith and recover the resonance sigil.",
                target="Ash Wraith",
                quantity=1,
            ),
        ],
        rewards={"gold": 120, "Stormglass Focus": 1},
        reputation={"Archivists": 40, "Wayfarers": 20},
    ),
    "Shadows over Ferrox": Quest(
        name="Shadows over Ferrox",
        giver="Captain Renn",
        summary="Sabotage the sentinel network orchestrating Vault Sentry patrols.",
        objectives=[
            QuestObjective(
                description="Recover three signal keystones from Hollow Corsairs.",
                target="Hollow Corsair",
                quantity=3,
            ),
            QuestObjective(
                description="Upload a false command at the canyon relay.",
                target="Interact",
                quantity=1,
            ),
        ],
        rewards={"gold": 95, "Wayfarer Rations": 4},
        reputation={"Wayfarers": 30},
    ),
}
