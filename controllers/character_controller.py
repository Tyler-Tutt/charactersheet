import flet as ft
from models.character_model import CharacterModel
from views.character_sheet_view import CharacterSheetView
from views.load_character_dialog import LoadCharacterDialog
import database

class CharacterController:
    def __init__(self, page: ft.Page):
        self.page = page
        
        # 1. Instantiate the Model
        self.model = CharacterModel()
        
        # 2. Instantiate the View (passing the controller's methods as callbacks)
        self.view = CharacterSheetView(
            model=self.model, 
            on_score_change_handler=self.handle_score_change, 
            on_header_change_handler=self.handle_header_change
        )

    def get_view(self):
        """Returns the main view so the app can render it."""
        return self.view

    # --- Event Handlers ---

    def handle_header_change(self, e: ft.ControlEvent):
        """Updates the model when a header text field changes."""
        attr_name = e.control.data
        new_value = e.control.value

        old_value = getattr(self.model, attr_name, None)
        
        # Type validation
        if attr_name in ['level', 'experience_points', 'armor_class', 'initiative', 'speed', 'max_hp', 'current_hp', 'temp_hp']:
            try:
                new_value = int(new_value)
            except (ValueError, TypeError):
                new_value = old_value 
                e.control.value = str(old_value) 
        
        setattr(self.model, attr_name, new_value)

    def handle_score_change(self, ability_name: str, new_score: int):
        """Updates the model when an ability score changes."""
        self.model.ability_scores[ability_name]["score"] = new_score
        print(f"Model Updated: {ability_name} is now {new_score}")

    def save_character(self, e):
        """Saves the current character data."""
        if self.model.save_character():
            self.page.open(
                ft.SnackBar(
                    ft.Text(f"Saved {self.model.charactername}!"), 
                    bgcolor=ft.Colors.GREEN_700
                )
            )
        else:
            self.page.open(
                ft.SnackBar(
                    ft.Text("Save failed. Check character name."), 
                    bgcolor=ft.Colors.ERROR
                )
            )

    def update_view_from_model(self):
        """Forces the view to update its UI components based on current model data."""
        self.view.header.update_header_data(self.model)
        self.view.achpspeed.update_stats_data(self.model)

        for card in self.view.ability_score_containers:
            ability_name = card.ability_name 
            if ability_name in self.model.ability_scores:
                ability_data = self.model.ability_scores[ability_name]
                card.update_card_data(
                    new_score=ability_data["score"],
                    new_skills_data=ability_data["skills"]
                )
        print(f"View updated from model for {self.model.charactername}")

    def open_load_dialog(self, e):
        """Handles opening the load dialog and managing its callbacks."""
        character_list = database.get_character_list()

        def handle_load(char_to_load):
            if self.model.load_character(char_to_load):
                self.update_view_from_model()
                self.page.close(dialog) 
                self.page.open(ft.SnackBar(ft.Text(f"Loaded {char_to_load}!"))) 
            else:
                self.page.open(ft.SnackBar(ft.Text(f"Failed to load {char_to_load}.")))

        def handle_cancel():
            self.page.close(dialog)

        dialog = LoadCharacterDialog(
            character_list=character_list,
            on_load_confirm=handle_load,
            on_cancel=handle_cancel
        )
        self.page.open(dialog)