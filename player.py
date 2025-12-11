# player.py
import json
from typing import Dict, List

class Player:
    def __init__(self, current_scene: str = "start"):
        self.current_scene = current_scene
        self.inventory = []   # list of item ids
        self.flags = {}       # dictionary of boolean flags
        self.stats = {"health": 100}  # example stat

    def to_dict(self) -> Dict:
        return {
            "current_scene": self.current_scene,
            "inventory": list(self.inventory),
            "flags": dict(self.flags),
            "stats": dict(self.stats)
        }

    @classmethod
    def from_dict(cls, d: Dict):
        p = cls(d.get("current_scene", "start"))
        p.inventory = d.get("inventory", [])
        p.flags = d.get("flags", {})
        p.stats = d.get("stats", {"health": 100})
        return p

    def has_item(self, item_id: str) -> bool:
        return item_id in self.inventory

    def add_item(self, item_id: str):
        if item_id not in self.inventory:
            self.inventory.append(item_id)

    def remove_item(self, item_id: str):
        if item_id in self.inventory:
            self.inventory.remove(item_id)

    def set_flag(self, name: str, value: bool):
        self.flags[name] = bool(value)

    def apply_effect(self, effect: Dict):
        """
        effect is a dict like {"type":"add_item","item":"lantern"} or {"type":"set_flag","name":"seen_cabin","value":true}
        Supported types: add_item, remove_item, set_flag, modify_stat, end_game
        """
        et = effect.get("type")
        if et == "add_item":
            item = effect.get("item")
            if item:
                self.add_item(item)
        elif et == "remove_item":
            item = effect.get("item")
            if item:
                self.remove_item(item)
        elif et == "set_flag":
            name = effect.get("name")
            val = effect.get("value", True)
            if name:
                self.set_flag(name, val)
        elif et == "modify_stat":
            name = effect.get("name")
            amount = effect.get("amount", 0)
            if name:
                self.stats[name] = self.stats.get(name, 0) + amount
        elif et == "end_game":
            # Represented as setting a special flag
            self.set_flag("_END_", effect.get("result", "neutral"))
