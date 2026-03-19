from typing import Final

# --- 5e Core Rules ---
BASE_AC: Final[int] = 10
BASE_ABILITY_SCORE: Final[int] = 10
ABILITY_MODIFIER_DIVISOR: Final[int] = 2

DEFAULT_SPEED: Final[int] = 30
DEFAULT_MAX_HP: Final[int] = 10

# Proficiency Bonus Math: 2 + ((Level - 1) // 4)
PROFICIENCY_BASE: Final[int] = 2
PROFICIENCY_LEVEL_DIVISOR: Final[int] = 4

# --- Character Abilities ---
ABILITIES: Final[list[str]] = [
    "Strength", "Dexterity", "Constitution",
    "Intelligence", "Wisdom", "Charisma"
]
# --- Character Skills ---
SKILLS: Final[dict[str, list[str]]] = {
    "Strength": ["Saving Throw", "Athletics"],
    "Dexterity": ["Saving Throw", "Acrobatics", "Sleight of Hand", "Stealth"],
    "Constitution": ["Saving Throw"],
    "Intelligence": ["Saving Throw", "Arcana", "History", "Investigation", "Nature", "Religion"],
    "Wisdom": ["Saving Throw", "Animal Handling", "Insight", "Medicine", "Perception", "Survival"],
    "Charisma": ["Saving Throw", "Deception", "Intimidation", "Performance", "Persuasion"]
}