from enum import Enum

# Multiple Inheritance (Strung Enum: Mixin). Used because of JSON library
class StatType(str, Enum):
    # Abilities
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"

    # Combat
    AC = "ac"
    SPEED = "speed"
    INITIATIVE = "initiative"
    MAX_HP = "max_hp"

    # Skills & Saving Throw
    SAVING_THROWS = "saving_throws"
    ATHLETICS = "athletics"
    ACROBATICS = "acrobatics"
    SLEIGHT_OF_HAND = "sleight_of_hand"
    STEALTH = "stealth"
    ARCANA = "arcana"
    HISTORY = "history"
    INVESTIGATION = "investigation"
    NATURE = "nature"
    RELIGION = "religion"
    ANIMAL_HANDLING = "animal_handling"
    INSIGHT = "insight"
    MEDICINE = "medicine"
    PERCEPTION = "perception"
    SURVIVAL = "survival"
    DECEPTION = "deception"
    INTIMIDATION = "intimidation"
    PERFORMANCE = "performance"
    PERSUASION = "persuasion"

# Multiple Inheritance (String Enum: Mixin)
class ModifierType(str, Enum):
    BONUS = "bonus"         
    OVERRIDE = "override"   
    MULTIPLIER = "multiplier" 
    ADVANTAGE = "advantage"
    DISADVANTAGE = "disadvantage"