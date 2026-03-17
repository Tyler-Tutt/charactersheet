from dataclasses import dataclass, field, asdict
from typing import Dict, List

@dataclass
class Skill:
    """Represents an individual character skill (Stealth, Arcana, Perception, etc.)"""
    base_proficient: bool = False

@dataclass
class Ability:
    """Represents an individual character Ability Score (Strength, Charisma, etc.)"""
    base_score: int = 10
    skills: Dict[str, Skill] = field(default_factory=dict)

@dataclass
class InventoryItem:
    """Represents an individual item within a character's inventory"""
    name: str
    description: str = ""
    short_description: str = ""
    is_equipped: bool = False
    modifiers: list = field(default_factory=list)

@dataclass
class CharacterModel:
    """Represents the pure data and domain logic of a Character"""
    
    # --- Core Attributes ---
    charactername: str = "Character Name"
    characterclass: str = "Character Class"
    level: int = 1
    background: str = "Background"
    player_name: str = "Player Name"
    race: str = "Race"
    alignment: str = "Alignment"
    experience_points: int = 0
    base_speed: int = 30
    base_max_hp: int = 10
    current_hp: int = 10
    temp_hp: int = 0

    # --- Modifier List ---
    active_modifiers: list = field(default_factory=list)
    
    # --- Inventory ---
    inventory: List[InventoryItem] = field(default_factory=list)

    # --- Ability & Skill Data ---
    ability_list: list = field(default_factory=lambda: [
        "Strength", "Dexterity", "Constitution",
        "Intelligence", "Wisdom", "Charisma"
    ])
    
    ability_scores_list: Dict[str, Ability] = field(default_factory=dict)

    def __post_init__(self):
        """Initializes the complex nested ability/skill dictionaries if not provided."""
        if not self.ability_scores_list:
            skill_map = {
                "Strength": ["Saving Throw", "Athletics"],
                "Dexterity": ["Saving Throw", "Acrobatics", "Sleight of Hand", "Stealth"],
                "Constitution": ["Saving Throw"],
                "Intelligence": ["Saving Throw", "Arcana", "History", "Investigation", "Nature", "Religion"],
                "Wisdom": ["Saving Throw", "Animal Handling", "Insight", "Medicine", "Perception", "Survival"],
                "Charisma": ["Saving Throw", "Deception", "Intimidation", "Performance", "Persuasion"]
            }
            
            for ability, skills in skill_map.items():
                ability_skills = {skill_name: Skill() for skill_name in skills}
                self.ability_scores_list[ability] = Ability(base_score=10, skills=ability_skills)

    # --- DERIVED PROPERTIES (The "Final" Values) ---
    @property
    def proficiency_bonus(self) -> int:
        """ Proficiency Bonus derived from character level."""
        # 5e math shortcut: PB = 2 + ((Level - 1) // 4)
        return 2 + ((self.level - 1) // 4)
        
    @property
    def final_speed(self) -> int:
        """Calculates final speed: Base + Modifiers"""
        bonus = sum(mod.get("value", 0) for mod in self.active_modifiers if mod.get("target") == "speed")
        return self.base_speed + bonus

    def get_final_ability_score(self, ability_name: str) -> int:
        base = self.ability_scores_list.get(ability_name).base_score if ability_name in self.ability_scores_list else 10
        bonus = sum(mod.get("value", 0) for mod in self.active_modifiers if mod.get("target") == ability_name)
        return base + bonus

    def is_skill_proficient(self, ability_name: str, skill_name: str) -> bool:
        ability = self.ability_scores_list.get(ability_name)
        if ability and skill_name in ability.skills:
            return ability.skills[skill_name].base_proficient
        return False

    @property
    def initiative(self) -> int:
        """Derived from FINAL Dexterity"""
        final_dex = self.get_final_ability_score("Dexterity")
        return (final_dex - 10) // 2

    @property
    def armor_class(self) -> int:
        """Derived from FINAL Dexterity and AC Modifiers"""
        final_dex = self.get_final_ability_score("Dexterity")
        dex_mod = (final_dex - 10) // 2
        bonus = sum(mod.get("value", 0) for mod in self.active_modifiers if mod.get("target") == "ac")
        return 10 + dex_mod + bonus

    def get_skill_modifier(self, ability_name: str, skill_name: str) -> int:
        """Calculates the final skill modifier using FINAL Ability Score and FINAL Proficiency."""
        final_score = self.get_final_ability_score(ability_name)
        base_modifier = (final_score - 10) // 2
        
        proficiency_bonus = self.proficiency_bonus if self.is_skill_proficient(ability_name, skill_name) else 0
        
        # Check active modifiers for specific skills OR all saving throws
        item_bonus = 0
        for mod in self.active_modifiers:
            if mod.get("target") == skill_name:
                item_bonus += mod.get("value", 0)
            elif skill_name == "Saving Throw" and mod.get("target") == "saving_throws":
                item_bonus += mod.get("value", 0)

        return base_modifier + proficiency_bonus + item_bonus
    
    def update_active_modifiers(self):
        """Rebuilds the active modifiers list based on equipped items."""
        # Condensed using Python List Comprehensions
        self.active_modifiers = [mod for item in self.inventory if item.is_equipped for mod in item.modifiers]

    # --- HELPER METHODS ---
    def format_modifier(self, mod: int) -> str:
        """Helper to safely format a modifier with a + or -"""
        return f"+{mod}" if mod >= 0 else str(mod)

    # --- SERIALIZATION / DESERIALIZATION ---
    def to_dict(self) -> dict:
        """Built-in standard for converting the dataclass to a JSON-ready dict."""
        return asdict(self)
        
    def load_from_dict(self, character_data: dict):
        """Updates the instance data in-place from a loaded dictionary."""
        if not character_data:
            return False

        # Load Standard Types
        for attr in ['charactername', 'characterclass', 'level', 'background', 
                     'player_name', 'race', 'alignment', 'experience_points', 
                     'base_speed', 'base_max_hp', 'current_hp', 'temp_hp']:
            if attr in character_data:
                setattr(self, attr, character_data[attr])
        
        # Load Complex Types (Abilities)
        if 'abilities' in character_data:
            for ability_name, ability_data in character_data['abilities'].items():
                if ability_name in self.ability_scores_list:
                    self.ability_scores_list[ability_name].base_score = ability_data.get('base_score', 10)
                    
                    for skill_name, skill_data in ability_data.get('skills', {}).items():
                        if skill_name in self.ability_scores_list[ability_name].skills:
                            self.ability_scores_list[ability_name].skills[skill_name].base_proficient = skill_data.get('base_proficient', False)
        
        # Load Complex Types (Inventory)
        self.inventory = []
        if 'inventory' in character_data:
            for item_data in character_data['inventory']:
                self.inventory.append(InventoryItem(**item_data))
                
        self.update_active_modifiers()
        return True