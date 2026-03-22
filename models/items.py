# models/items.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Modifier:
    """A strict schema for any stat-altering buff or debuff."""
    target: str   # Eventually, this should be an Enum! (e.g., StatType.AC)
    value: int
    source: str

@dataclass
class InventoryItem:
    """Represents an individual item within a character's inventory"""
    name: str
    description: str = ""
    short_description: str = ""
    is_equipped: bool = False
    modifiers: List[Modifier] = field(default_factory=list)

    def __post_init__(self):
        """Automatically convert raw dictionaries from the DB into Modifier objects."""
        # When loaded from JSON, modifiers might be dictionaries convert them
        if self.modifiers and isinstance(self.modifiers[0], dict):
            self.modifiers = [Modifier(**mod_dict) for mod_dict in self.modifiers]