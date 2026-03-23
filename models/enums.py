from enum import Enum, auto

class StatType(str, Enum):
    # Core Stats
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    # Combat
    AC = "ac"
    SPEED = "speed"
    INITIATIVE = "initiative"
    MAX_HP = "max_hp"
    # Skills/Saves
    SAVING_THROWS = "saving_throws"
    STEALTH = "stealth"
    # Add all other skills/targets here...

class ModifierType(str, Enum):
    BONUS = "bonus"         # Additive (+1, -2)
    OVERRIDE = "override"   # Sets a stat to a specific number (e.g., Gauntlets of Ogre Power)
    MULTIPLIER = "multiplier" # e.g., double carrying capacity
    ADVANTAGE = "advantage"   # Boolean logic
    DISADVANTAGE = "disadvantage"