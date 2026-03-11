import flet as ft
from models.character_model import CharacterModel
from views.character_sheet_view import CharacterSheetView
from views.load_character_modal import LoadCharacterModal
import database

class CharacterSheetController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.model = CharacterModel()
        
        self.view = CharacterSheetView(
            model=self.model, 
            on_score_change_handler=self.handle_score_change, 
            on_header_change_handler=self.handle_header_change,
            on_skill_proficiency_change_handler=self.handle_skill_proficiency_change
        )

    def get_view(self):
        return self.view

    # --- Event Handlers ---

    def handle_header_change(self, e: ft.ControlEvent):
        """Updates the model when a header text field changes."""
        attr_name = e.control.data
        new_value = e.control.value
        old_value = getattr(self.model, attr_name, None)
        
        # Type validation
        if attr_name in ['level', 'experience_points', 'speed', 'max_hp', 'current_hp', 'temp_hp']:
            try:
                new_value = int(new_value)
            except (ValueError, TypeError):
                new_value = old_value 
                e.control.value = str(old_value) 
        
        setattr(self.model, attr_name, new_value)

        # SENIOR TIP: If level changes, Proficiency Bonus changes! 
        if attr_name == 'level':
            # 🟢 1. Update the Proficiency Bonus field itself
            self.view.update_proficiency_bonus()
            
            # 2. Tell all Ability Cards to recalculate their skill modifiers
            for card in self.view.ability_score_containers:
                card.update_card_data()

    def handle_skill_proficiency_change(self, e: ft.ControlEvent):
        """Fired when a user clicks a skill proficiency checkbox."""
        # e.control.data contains our dict {"ability": "Dexterity", "skill": "Stealth"}
        ability_name = e.control.data["ability"]
        skill_name = e.control.data["skill"]
        is_proficient = e.control.value

        # 1. Update Model
        self.model.ability_scores[ability_name]["skills"][skill_name]["proficient"] = is_proficient
        
        # 2. Tell only the affected card to update its UI
        for card in self.view.ability_score_containers:
            if card.ability_name == ability_name:
                card.update_card_data()
                break

    def handle_score_change(self, ability_name: str, new_score: int):
        """Updates the model and triggers UI updates when an Ability Score changes."""
        if ability_name in self.model.ability_scores:
            self.model.ability_scores[ability_name]["score"] = new_score

        if ability_name == "Dexterity":
            self.view.achpspeed.update_stats_data(self.model)
            
        for card in self.view.ability_score_containers:
            if card.ability_name == ability_name:
                card.update_card_data()
                break 

    def save_character(self, e):
        if self.model.save_character():
            self.page.open(ft.SnackBar(ft.Text(f"Saved {self.model.charactername}!"), bgcolor=ft.Colors.GREEN_700))
        else:
            self.page.open(ft.SnackBar(ft.Text("Save failed. Check character name."), bgcolor=ft.Colors.ERROR))

    def update_view_from_model(self):
        """Forces the view to update its UI components based on current model data."""
        self.view.header.update_header_data(self.model)
        self.view.achpspeed.update_stats_data(self.model)

        for card in self.view.ability_score_containers:
            card.update_card_data()

    def open_load_modal(self, e):
        character_list = database.get_character_list()

        def handle_load(char_to_load):
            if self.model.load_character(char_to_load):
                self.update_view_from_model()
                self.page.close(modal) 
                self.page.open(ft.SnackBar(ft.Text(f"Loaded {char_to_load}!"))) 
            else:
                self.page.open(ft.SnackBar(ft.Text(f"Failed to load {char_to_load}.")))

        def handle_cancel():
            self.page.close(modal)

        modal = LoadCharacterModal(
            character_list=character_list,
            on_load_confirm=handle_load,
            on_cancel=handle_cancel
        )
        self.page.open(modal)