from dataclasses import dataclass
from typing import Any
from .enums import StatType, ModifierType

@dataclass
class EffectModifier:
    """Class for altering a character's state."""
    source_name: str
    target: StatType
    modifier_type: ModifierType
    value: Any
    duration: int = -1

    def __post_init__(self):
        if isinstance(self.target, str):
            self.target = StatType(self.target)
        if isinstance(self.modifier_type, str):
            self.modifier_type = ModifierType(self.modifier_type)