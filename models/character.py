from dataclasses import dataclass, field, asdict
from typing import Dict, List
import constants as constant
from models.items import InventoryItem, Modifier
from models.stats import Ability, Skill

@dataclass
class CharacterModel:
    """Represents the current data and score-logic of a Character"""
    
    # --- Core Attributes ---
    charactername: str = "Character Name"
    characterclass: str = "Character Class"
    level: int = 1
    background: str = "Background"
    player_name: str = "Player Name"
    race: str = "Race"
    alignment: str = "Alignment"
    experience_points: int = 0
    base_speed: int = constant.DEFAULT_SPEED
    base_max_hp: int = constant.DEFAULT_MAX_HP
    current_hp: int = constant.DEFAULT_MAX_HP
    temp_hp: int = 0

    # --- Modifier List ---
    active_modifiers: list = field(default_factory=list)
    
    # --- Inventory ---
    inventory: List[InventoryItem] = field(default_factory=list)

    # --- Ability & Skill Data ---
    # Fetch directly from constants instead of hardcoding
    ability_list: list = field(default_factory=lambda: constant.ABILITIES.copy())
    
    ability_scores_list: Dict[str, Ability] = field(default_factory=dict)

    def __post_init__(self):
        """Initializes the complex nested ability/skill dictionaries if not provided."""
        if not self.ability_scores_list:
            # We no longer need the massive dictionary definition here!
            for ability, skills in constant.SKILLS.items():
                ability_skills = {skill_name: Skill() for skill_name in skills}
                self.ability_scores_list[ability] = Ability(
                    base_score=constant.BASE_ABILITY_SCORE, 
                    skills=ability_skills
                )

    # --- DERIVED PROPERTIES (The "Final" Values) ---
    @property
    def proficiency_bonus(self) -> int:
        """ Proficiency Bonus derived from character level."""
        return constant.PROFICIENCY_BASE + ((self.level - 1) // constant.PROFICIENCY_LEVEL_DIVISOR)
        
    @property
    def final_speed(self) -> int:
        """Calculates final speed: Base + Modifiers"""
        bonus = sum(mod.value for mod in self.active_modifiers if mod.target == "speed")
        return self.base_speed + bonus

    def get_final_ability_score(self, ability_name: str) -> int:
        base = self.ability_scores_list.get(ability_name).base_score if ability_name in self.ability_scores_list else constant.BASE_ABILITY_SCORE
        bonus = sum(mod.value for mod in self.active_modifiers if mod.target == ability_name)
        return base + bonus

    def is_skill_proficient(self, ability_name: str, skill_name: str) -> bool:
        ability = self.ability_scores_list.get(ability_name)
        if ability and skill_name in ability.skills:
            return ability.skills[skill_name].base_proficiency
        return False

    @property
    def initiative(self) -> int:
        """Derived from FINAL Dexterity"""
        final_dex = self.get_final_ability_score("Dexterity")
        return (final_dex - constant.BASE_ABILITY_SCORE) // constant.ABILITY_MODIFIER_DIVISOR

    @property
    def armor_class(self) -> int:
        """Derived from FINAL Dexterity and AC Modifiers"""
        final_dex = self.get_final_ability_score("Dexterity")
        dex_mod = (final_dex - constant.BASE_ABILITY_SCORE) // constant.ABILITY_MODIFIER_DIVISOR
        bonus = sum(mod.value for mod in self.active_modifiers if mod.target =="ac")
        return constant.BASE_AC + dex_mod + bonus
    
    @property
    def carrying_capacity(self) -> int:
        """Strength score * 15 + any active modifiers."""
        final_str = self.get_final_ability_score("Strength")
        base_capacity = final_str * 15
        bonus = sum(mod.value for mod in self.active_modifiers if mod.target == "carrying_capacity")
        return base_capacity + bonus

    def get_skill_modifier(self, ability_name: str, skill_name: str) -> int:
        """Ability Score Modifier + Proficiency."""
        final_score = self.get_final_ability_score(ability_name)
        base_modifier = (final_score - constant.BASE_ABILITY_SCORE) // constant.ABILITY_MODIFIER_DIVISOR
        
        proficiency_bonus = self.proficiency_bonus if self.is_skill_proficient(ability_name, skill_name) else 0
        
        # Check active modifiers for specific skills OR all saving throws
        item_bonus = 0
        for mod in self.active_modifiers:
            if mod.target == skill_name:
                item_bonus += mod.value
            elif skill_name == "Saving Throw" and mod.target == "saving_throws":
                item_bonus += mod.value

        return base_modifier + proficiency_bonus + item_bonus
    
    def update_active_modifiers(self):
        """Rebuilds the active modifiers list based on equipped items."""
        self.active_modifiers = [mod for item in self.inventory if item.is_equipped for mod in item.modifiers]

    # --- HELPER METHODS ---
    def format_modifier(self, mod: int) -> str:
        """Helper to safely format a modifier with a + or -"""
        return f"+{mod}" if mod >= 0 else str(mod)

    # --- SERIALIZATION / DESERIALIZATION ---
    def convert_to_dictionary(self) -> dict:
        """Built-in standard for converting the dataclass to a JSON-ready dict."""
        return asdict(self)
        
    def load_from_dictionary(self, character_data: dict):
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
                    self.ability_scores_list[ability_name].base_score = ability_data.get('base_score', constant.BASE_ABILITY_SCORE)
                    
                    for skill_name, skill_data in ability_data.get('skills', {}).items():
                        if skill_name in self.ability_scores_list[ability_name].skills:
                            self.ability_scores_list[ability_name].skills[skill_name].base_proficiency = skill_data.get('base_proficient', False)
        
        # Load Complex Types (Inventory)
        self.inventory = []
        if 'inventory' in character_data:
            for item_data in character_data['inventory']:
                self.inventory.append(InventoryItem(**item_data))
                
        self.update_active_modifiers()
        return True