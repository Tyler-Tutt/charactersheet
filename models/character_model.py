import database
from dataclasses import dataclass, field, asdict
from typing import Dict

@dataclass
class Skill:
    base_proficient: bool = False

@dataclass
class Ability:
    base_score: int = 10
    skills: Dict[str, Skill] = field(default_factory=dict)

class CharacterModel():
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

        # --- Ability & Skill Data ---
        self.abilities_list = [
            "Strength", "Dexterity", "Constitution",
            "Intelligence", "Wisdom", "Charisma"
        ]
        self.skills_map = {
            "Strength": ["Saving Throw", "Athletics"],
            "Dexterity": ["Saving Throw", "Acrobatics", "Sleight of Hand", "Stealth"],
            "Constitution": ["Saving Throw"],
            "Intelligence": ["Saving Throw", "Arcana", "History", "Investigation", "Nature", "Religion"],
            "Wisdom": ["Saving Throw", "Animal Handling", "Insight", "Medicine", "Perception", "Survival"],
            "Charisma": ["Saving Throw", "Deception", "Intimidation", "Performance", "Persuasion"]
        }

        self.ability_scores: Dict[str, Ability] = {}
        
        for ability in self.abilities_list:
            # Create a dictionary of Skill objects mapped to their names
            ability_skills = {
                skill_name: Skill() for skill_name in self.skills_map[ability]
            }
            # Assign the Ability object to the main dictionary
            self.ability_scores[ability] = Ability(base_score=10, skills=ability_skills)

        if character_to_load:
            self.load_character(character_to_load)

    # --- DERIVED PROPERTIES ---
    @property
    def proficiency_bonus(self) -> int:
        """ Proficiency Bonus derived based on character level."""
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
    
    # --- DERIVED PROPERTIES (The "Final" Values) ---
    
    @property
    def final_speed(self) -> int:
        """Calculates final speed: Base + Modifiers"""
        bonus = sum(mod.get("value", 0) for mod in self.active_modifiers if mod.get("target") == "speed")
        return self.base_speed + bonus

    def get_final_ability_score(self, ability_name: str) -> int:
        # NEW: access the object attribute .base_score
        base = self.ability_scores.get(ability_name).base_score if ability_name in self.ability_scores else 10
        bonus = sum(mod.get("value", 0) for mod in self.active_modifiers if mod.get("target") == ability_name)
        return base + bonus

    def is_skill_proficient(self, ability_name: str, skill_name: str) -> bool:
        # NEW: access .skills and .base_proficient cleanly
        ability = self.ability_scores.get(ability_name)
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
        """Derived from FINAL Dexterity (Placeholder for armor calculation)"""
        final_dex = self.get_final_ability_score("Dexterity")
        dex_mod = (final_dex - 10) // 2
        bonus = sum(mod.get("value", 0) for mod in self.active_modifiers if mod.get("target") == "ac")
        return 10 + dex_mod + bonus

    def get_skill_modifier(self, ability_name: str, skill_name: str) -> int:
        """Calculates the final skill modifier using FINAL Ability Score and FINAL Proficiency."""
        final_score = self.get_final_ability_score(ability_name)
        base_mod = (final_score - 10) // 2
        
        if self.is_skill_proficient(ability_name, skill_name):
            return base_mod + self.proficiency_bonus
        return base_mod

    # --- HELPER METHODS ---
    def format_modifier(self, mod: int) -> str:
        """Helper to safely format a modifier with a + or -"""
        return f"+{mod}" if mod >= 0 else str(mod)

    # --- SAVE / LOAD ---
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
                if ab_name in self.ability_scores:
                    self.ability_scores[ab_name].base_score = ab_data.get('base_score', 10)
                    
                    for sk_name, sk_data in ab_data.get('skills', {}).items():
                        if sk_name in self.ability_scores[ab_name].skills:
                            self.ability_scores[ab_name].skills[sk_name].base_proficient = sk_data.get('base_proficient', False)
        return True
        
    def convert_to_dictionary(self):
        return {
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
            'abilities': {k: asdict(v) for k, v in self.ability_scores.items()}
        }

    def save_character(self):
        if not self.charactername or self.charactername == "Character Name":
            print("Save Error: Please enter a character name before saving.")
            return False

        character_data = self.convert_to_dictionary()
        database.save_character(self.charactername, character_data)
        print(f"Success: Character '{self.charactername}' was saved.")
        return True