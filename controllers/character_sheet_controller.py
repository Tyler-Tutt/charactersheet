import flet as ft
from models.character_model import CharacterModel
from views.character_sheet_view import CharacterSheetView
from views.load_character_modal import LoadCharacterModal
import database

class CharacterSheetController:
    '''
    The central orchestrator that manages the flow of data between the character model and the user interface. 
    It translates user interactions into model updates and ensures the view reflects the most current state.
    '''
    def __init__(self, page: ft.Page):
        '''
        Initializes the controller by linking the Flet page, instantiating the data model, and creating the main character sheet view. 
        It also sets the initial application state, starting the user in a non-editable viewing mode.
        '''
        self.page = page
        self.model = CharacterModel()
        self.is_edit_mode = False
        
        self.view = CharacterSheetView(
            model=self.model, 
            controller=self
        )

        self.view.set_edit_mode(self.is_edit_mode)

    def toggle_edit_mode(self, e):
        '''
        Switches the application between read-only and interactive states by updating the is_edit_mode flag. 
        It dynamically modifies UI elements like icons and tooltips while providing visual feedback to the user via a SnackBar.
        '''
        self.is_edit_mode = not self.is_edit_mode
        self.view.set_edit_mode(self.is_edit_mode)
        
        # Update the Appbar icon dynamically
        e.control.icon = ft.Icons.EDIT if self.is_edit_mode else ft.Icons.EDIT_OFF
        e.control.tooltip = "Switch to View Mode" if self.is_edit_mode else "Switch to Edit Mode"
        e.control.update() 
        
        mode_text = "Edit Mode Enabled" if self.is_edit_mode else "Viewing Mode"
        self.page.open(ft.SnackBar(ft.Text(mode_text), duration=1500))

    def get_view(self):
        '''
        Getter method that returns the top-level CharacterSheetView component managed by the controller. 
        Allows the main entry point of the app to easily add the entire character sheet to the page
        '''
        return self.view

    # --- Event Handlers ---

    def handle_header_change(self, e: ft.ControlEvent):
        '''
        Updates the character model when general information fields, such as "Level" or "Race," are modified in the UI. 
        Includes basic type validation to ensure numeric fields remain valid integers before triggering dependent UI refreshes.
        '''
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

        if attr_name == 'speed':
            self.model.base_speed = new_value
        else:
            setattr(self.model, attr_name, new_value)

        if attr_name == 'level':
            self.view.update_proficiency_bonus()
            
            for card in self.view.ability_score_containers:
                card.update_card_data()

    def handle_skill_proficiency_change(self, e: ft.ControlEvent):
        '''
        Responds to users toggling skill proficiency checkboxes by updating the specific skill's status within the data model. 
        Optimizes performance by instructing only the relevant ability score container to redraw its UI.
        '''
        # e.control.data contains our dict {"ability": "Dexterity", "skill": "Stealth"}
        ability_name = e.control.data["ability"]
        skill_name = e.control.data["skill"]
        is_proficient = e.control.value

        # 1. Update Model
        self.model.ability_scores[ability_name]["skills"][skill_name]["base_proficient"] = is_proficient
        
        # 2. Tell only the affected card to update its UI
        for card in self.view.ability_score_containers:
            if card.ability_name == ability_name:
                card.update_card_data()
                break

    def handle_ability_score_change(self, ability_name: str, new_score: int):
        '''
        Synchronizes the model when a base ability score (e.g., Strength) changes and forces updates to dependent stats like modifiers and Armor Class. 
        Ensures that a change in one stat correctly ripples through all related calculations in the view.
        '''
        if ability_name in self.model.ability_scores:
            self.model.ability_scores[ability_name]["base_score"] = new_score

        if ability_name == "Dexterity":
            self.view.achpspeed.update_stats_data(self.model)
            
        for card in self.view.ability_score_containers:
            if card.ability_name == ability_name:
                card.update_card_data()
                break 

    def save_character(self, e):
        '''
        Directs the model to serialize its current data and persist it to the SQLite database. 
        Displays a success or error message to the user based on whether the character name was valid and the save operation succeeded.
        '''
        if self.model.save_character():
            self.page.open(ft.SnackBar(ft.Text(f"Saved {self.model.charactername}!"), bgcolor=ft.Colors.GREEN_700))
        else:
            self.page.open(ft.SnackBar(ft.Text("Save failed. Check character name."), bgcolor=ft.Colors.ERROR))

    def update_view_from_model(self):
        '''
        Utility function that forces every major component in the view to refresh its data from the current model state. 
        Primarily used after a new character is loaded to ensure the UI displays the correct information.
        '''
        self.view.header.update_header_data(self.model)
        self.view.achpspeed.update_stats_data(self.model)

        for card in self.view.ability_score_containers:
            card.update_card_data()

    def open_load_modal(self, e):
        '''
        Retrieves the list of saved characters from the database and presents them in a selection dialog. 
        Manages the logic for confirming a load operation, updating the UI with the selected character's data, or canceling the request.
        '''
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