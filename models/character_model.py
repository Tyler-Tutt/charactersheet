import database
from dataclasses import dataclass, field, asdict
from typing import Dict, List

@dataclass
class InventoryItem:
    '''
    Represents an individual item within a character's inventory
    '''
    name: str
    description: str = ""
    short_description: str = ""
    is_equipped: bool = False
    modifiers: list = field(default_factory=list)

@dataclass
class Skill:
    '''
    Represents an individual character skill (Stealth, Arcana, Perception, etc.)
    '''
    base_proficient: bool = False

@dataclass
class Ability:
    '''
    Represents an individual character Ability Score (Strength, Charisma, etc.)
    '''
    base_score: int = 10
    skills: Dict[str, Skill] = field(default_factory=dict)

class CharacterModel():
    '''
    Represents & Defines the data (fields) of a Character
    '''
    def __init__(self, character_to_load=None):
        # --- Character Attributes ---
        self.charactername = "Character Name"
        self.characterclass = "Character Class"
        self.level = 1
        self.background = "Background"
        self.player_name = "Player Name"
        self.race = "Race"
        self.alignment = "Alignment"
        self.experience_points = 0
        self.base_speed = 30
        self.base_max_hp = 10
        self.current_hp = 10
        self.temp_hp = 0

        # --- Future-Proofing: Modifier List ---
        # Later, you will append dicts or objects here like {"target": "speed", "value": 10, "source": "Boots of Speed"}
        self.active_modifiers = []
        # Inventory list
        self.inventory: List[InventoryItem] = []

        # --- Ability & Skill Data ---
        self.ability_list = [
            "Strength", "Dexterity", "Constitution",
            "Intelligence", "Wisdom", "Charisma"
        ]
        self.skill_map = {
            "Strength": ["Saving Throw", "Athletics"],
            "Dexterity": ["Saving Throw", "Acrobatics", "Sleight of Hand", "Stealth"],
            "Constitution": ["Saving Throw"],
            "Intelligence": ["Saving Throw", "Arcana", "History", "Investigation", "Nature", "Religion"],
            "Wisdom": ["Saving Throw", "Animal Handling", "Insight", "Medicine", "Perception", "Survival"],
            "Charisma": ["Saving Throw", "Deception", "Intimidation", "Performance", "Persuasion"]
        }

        self.ability_scores_list: Dict[str, Ability] = {}

        for ability in self.ability_list:
            # Create a dictionary of Skill objects mapped to their names
            ability_skills = {
                skill_name: Skill() for skill_name in self.skill_map[ability]
            }
            # Assign the Ability object to the main dictionary
            self.ability_scores_list[ability] = Ability(base_score=10, skills=ability_skills)

        if character_to_load:
            self.load_character(character_to_load)

    # --- DERIVED PROPERTIES (The "Final" Values) ---
    @property
    def proficiency_bonus(self) -> int:
        """ Proficiency Bonus derived on character level."""
        level = self.level
        if 1 <= level <= 4:
            return 2
        elif 5 <= level <= 8:
            return 3
        elif 9 <= level <= 12:
            return 4
        elif 13 <= level <= 16:
            return 5
        elif 17 <= level <= 20:
            return 6
        return 0
        
    @property
    def final_speed(self) -> int:
        """Calculates final speed: Base + Modifiers"""
        bonus = sum(mod.get("value", 0) for mod in self.active_modifiers if mod.get("target") == "speed")
        return self.base_speed + bonus

    def get_final_ability_score(self, ability_name: str) -> int:
        # Access the object attribute of '.base_score'
        base = self.ability_scores_list.get(ability_name).base_score if ability_name in self.ability_scores_list else 10
        bonus = sum(mod.get("value", 0) for mod in self.active_modifiers if mod.get("target") == ability_name)
        return base + bonus

    def is_skill_proficient(self, ability_name: str, skill_name: str) -> bool:
        # Access '.skills' and '.base_proficient' cleanly
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
        """
        Derived from FINAL Dexterity (Placeholder for armor calculation)
        """
        final_dex = self.get_final_ability_score("Dexterity")
        dex_mod = (final_dex - 10) // 2
        bonus = sum(mod.get("value", 0) for mod in self.active_modifiers if mod.get("target") == "ac")
        return 10 + dex_mod + bonus

    def get_skill_modifier(self, ability_name: str, skill_name: str) -> int:
        """
        Calculates the final skill modifier using FINAL Ability Score and FINAL Proficiency.
        """
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
        self.active_modifiers = []
        for item in self.inventory:
            if item.is_equipped:
                self.active_modifiers.extend(item.modifiers)

    # --- HELPER METHODS ---
    def format_modifier(self, mod: int) -> str:
        """Helper to safely format a modifier with a + or -"""
        return f"+{mod}" if mod >= 0 else str(mod)

    # --- LOAD / SAVE / CONVERT TO DICTIONARY---
    def load_character(self, character_name):
        data = database.load_character(character_name)
        if not data:
            print(f"Load Error: Could not find data for {character_name}.")
            return False    

        self.charactername = data.get('charactername', "Unknown")
        self.characterclass = data.get('characterclass', "Class")
        self.level = data.get('level', 1)
        self.background = data.get('background', "Background")
        self.player_name = data.get('player_name', "Player Name")
        self.race = data.get('race', "Race")
        self.alignment = data.get('alignment', "Alignment")
        self.experience_points = data.get('experience_points', 0)
        self.base_speed = data.get('base_speed', 30)
        self.base_max_hp = data.get('base_max_hp', 10)
        self.current_hp = data.get('current_hp', 10)
        self.temp_hp = data.get('temp_hp', 0)
        
        if 'abilities' in data:
            for ab_name, ab_data in data['abilities'].items():
                if ab_name in self.ability_scores_list:
                    self.ability_scores_list[ab_name].base_score = ab_data.get('base_score', 10)
                    
                    for sk_name, sk_data in ab_data.get('skills', {}).items():
                        if sk_name in self.ability_scores_list[ab_name].skills:
                            self.ability_scores_list[ab_name].skills[sk_name].base_proficient = sk_data.get('base_proficient', False)
        
        self.inventory = []
        if 'inventory' in data:
            for item_data in data['inventory']:
                self.inventory.append(InventoryItem(**item_data))
                
        self.update_active_modifiers() # Refresh modifiers after loading
        
        return True
        
    def convert_to_dictionary(self):
        data = {
            'charactername': self.charactername,
            'characterclass': self.characterclass,
            'level': self.level,
            'background': self.background,
            'player_name': self.player_name,
            'race': self.race,
            'alignment': self.alignment,
            'experience_points': self.experience_points,
            'base_speed': self.base_speed,
            'base_max_hp': self.base_max_hp,
            'current_hp': self.current_hp,
            'temp_hp': self.temp_hp,
            'abilities': {k: asdict(v) for k, v in self.ability_scores_list.items()},
            'inventory': [asdict(item) for item in self.inventory]
        }

        data['charactername'] = self.charactername
        data['characterclass'] = self.characterclass
        data['level'] = self.level
        data['background'] = self.background
        data['player_name'] = self.player_name
        data['race'] = self.race
        data['alignment'] = self.alignment
        data['experience_points'] = self.experience_points
        data['base_speed'] = self.base_speed
        data['base_max_hp'] = self.base_max_hp
        data['current_hp'] = self.current_hp
        data['temp_hp'] = self.temp_hp

        return data

    def save_character(self):
        if not self.charactername or self.charactername == "Character Name":
            print("Save Error: Please enter a character name before saving.")
            return False

        character_data = self.convert_to_dictionary()
        database.save_character(self.charactername, character_data)
        print(f"Success: Character '{self.charactername}' was saved.")
        return True