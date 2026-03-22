from dataclasses import dataclass, field
from typing import Dict
import constants as constant

@dataclass
class Skill:
    """Represents an individual character skill (Stealth, Arcana, Perception, etc.)"""
    base_proficiency: bool = False

@dataclass
class Ability:
    """Represents an individual character Ability Score (Strength, Charisma, etc.)"""
    base_score: int = constant.BASE_ABILITY_SCORE
    skills: Dict[str, Skill] = field(default_factory=dict)