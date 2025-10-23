from __future__ import annotations

from typing import Dict

from game.data.items import ITEMS, Item


class Inventory:
    def __init__(self) -> None:
        self.items: Dict[str, int] = {}
        self.gold: int = 0

    def add_item(self, item_name: str, quantity: int = 1) -> None:
        if item_name not in ITEMS:
            raise KeyError(item_name)
        self.items[item_name] = self.items.get(item_name, 0) + quantity

    def remove_item(self, item_name: str, quantity: int = 1) -> None:
        if self.items.get(item_name, 0) < quantity:
            raise ValueError("Not enough items to remove")
        self.items[item_name] -= quantity
        if self.items[item_name] <= 0:
            del self.items[item_name]

    def sell_item(self, item_name: str, quantity: int = 1) -> int:
        self.remove_item(item_name, quantity)
        item = ITEMS[item_name]
        payout = int(item.value * 0.6) * quantity
        self.gold += payout
        return payout

    def buy_item(self, item_name: str, quantity: int = 1) -> None:
        item = ITEMS[item_name]
        total_cost = item.value * quantity
        if self.gold < total_cost:
            raise ValueError("Insufficient gold")
        self.gold -= total_cost
        self.add_item(item_name, quantity)

    def describe(self) -> str:
        lines = [f"Gold: {self.gold}"]
        for item_name, count in sorted(self.items.items()):
            item = ITEMS[item_name]
            lines.append(f"{item_name} x{count} ({item.rarity}) - {item.description}")
        return "\n".join(lines)

    def get_item(self, item_name: str) -> Item:
        return ITEMS[item_name]
