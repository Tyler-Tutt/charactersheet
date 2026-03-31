from dataclasses import dataclass
from typing import Any
from .enums import StatType, ArithmeticType

@dataclass
class EffectModifier:
    """Standardized Class for Effects from different sources to modify character stats."""
    source_name: str
    target: StatType
    arithmetic_type: ArithmeticType
    value: Any
    duration: int = -1

    def __post_init__(self):
        if isinstance(self.target, str):
            self.target = StatType(self.target)
        if isinstance(self.arithmetic_type, str):
            self.arithmetic_type = ArithmeticType(self.arithmetic_type)