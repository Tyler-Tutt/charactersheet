from dataclasses import dataclass
from typing import Any
from .enums import StatType, ModifierType

@dataclass
class EffectModifier:
    """Standardized class for altering a character's state."""
    source_name: str
    target: StatType
    mod_type: ModifierType
    value: Any
    duration: int = -1

    def __post_init__(self):
        if isinstance(self.target, str):
            self.target = StatType(self.target)
        if isinstance(self.mod_type, str):
            self.mod_type = ModifierType(self.mod_type)