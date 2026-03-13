import flet as ft
from typing import TYPE_CHECKING
from models.character_model import CharacterModel
if TYPE_CHECKING:
    from controllers.character_sheet_controller import CharacterSheetController

class AbilityScoreContainer(ft.Container):
    def __init__(self, model: CharacterModel, ability_name: str, controller: 'CharacterSheetController'):
        super().__init__(
            padding=10,
            bgcolor=ft.Colors.LIGHT_GREEN,
            border=ft.border.all(2, ft.Colors.OUTLINE),
            border_radius=8
        )
        self.model = model
        self.ability_name = ability_name
        self.controller = controller
        
        # We will store references to the skill modifier fields here so we can update them later
        self.skill_modifier_fields = {}
        # <-- A list to track checkboxes
        self.skill_checkboxes = [] 
        
        # --- Internal UI Elements ---
        initial_score = self.model.ability_scores[ability_name]["base_score"]
        
        self.ability_name_text = ft.Text(ability_name.upper(), size=16, weight=ft.FontWeight.BOLD)
        self.modifier_text = ft.Text(self.model.format_modifier((initial_score - 10) // 2), size=20)
        self.score_field = ft.TextField(
            value=str(initial_score),
            text_align=ft.TextAlign.CENTER,
            width=100,
            on_change=self._internal_score_change
        )
        
        # --- Build Skills UI ---
        self.skills_controls = []
        skills_data = self.model.ability_scores[ability_name]["skills"]
        
        for skill_name, skill_info in skills_data.items():
            
            # The derived modifier value
            mod_val = self.model.get_skill_modifier(self.ability_name, skill_name)
            
            # Read-only field for the modifier
            mod_field = ft.TextField(
                value=self.model.format_modifier(mod_val), 
                read_only=True, 
                width=60, 
                text_align=ft.TextAlign.CENTER, 
                col={"sm": 3, "md": 3}
            )
            self.skill_modifier_fields[skill_name] = mod_field
            
            # The Checkbox. We use 'data' to pass a dictionary so the handler knows EXACTLY what was clicked.
            prof_checkbox = ft.Checkbox(
                value=skill_info["base_proficient"], 
                data={"ability": self.ability_name, "skill": skill_name},
                on_change=self.controller.handle_skill_proficiency_change,
                col={"sm": 2, "md": 2}
            )
            self.skill_checkboxes.append(prof_checkbox) # <-- Track the checkbox
            
            self.skills_controls.append(
                ft.ResponsiveRow(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        prof_checkbox,
                        mod_field,
                        ft.Text(skill_name, selectable=True, col={"sm": 7, "md": 7})
                    ]
                )
            )
            
        # --- Layout ---
        self.content = ft.ResponsiveRow(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Column(
                    col={"sm": 12, "md": 4},
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.ability_name_text,
                        self.modifier_text,
                        self.score_field
                        ]
                ),
                ft.Column(
                    col={"sm": 12, "md": 8},
                    controls=
                        self.skills_controls
                ),
            ]
        )

    def _internal_score_change(self, e: ft.ControlEvent):
        """Handles the text field change internally, updates its own UI, then notifies the controller."""
        raw_value = e.control.value
        try:
            new_score = int(raw_value) if raw_value != "" else 0
        except ValueError:
            new_score = 10
            self.score_field.value = str(new_score)

        # 1. Update this specific component's UI instantly
        self.modifier_text.value = self.model.format_modifier((new_score - 10) // 2)
        
        # 2. Tell the main controller the data changed
        if self.controller:
            self.controller.handle_ability_score_change(self.ability_name, new_score)

    def update_card_data(self):
        """Pulls fresh data from the model and updates the UI based on current mode."""
        # Check if we are currently in edit mode by checking our own text field's state
        is_edit = not self.score_field.read_only
        
        # Update main score based on edit state
        if is_edit:
            score = self.model.ability_scores[self.ability_name]["base_score"]
        else:
            score = self.model.get_final_ability_score(self.ability_name)
            
        self.score_field.value = str(score)
        self.modifier_text.value = self.model.format_modifier((score - 10) // 2)
        
        # Update checkboxes and derived modifiers
        for skill_name, mod_field in self.skill_modifier_fields.items():
            # Get fresh derived modifier
            new_mod_val = self.model.get_skill_modifier(self.ability_name, skill_name)
            mod_field.value = self.model.format_modifier(new_mod_val)
            
        for checkbox in self.skill_checkboxes:
            skill_name = checkbox.data["skill"]
            if is_edit:
                checkbox.value = self.model.ability_scores[self.ability_name]["skills"][skill_name]["base_proficient"]
            else:
                checkbox.value = self.model.is_skill_proficient(self.ability_name, skill_name)
        
        if self.page:
            self.update()

    def set_edit_mode(self, is_edit: bool):
        self.score_field.read_only = not is_edit
        
        # --- The Magic Swap for Ability Scores ---
        if is_edit:
            # Show the raw, editable base score
            base_val = self.model.ability_scores[self.ability_name]["base_score"]
            self.score_field.value = str(base_val)
        else:
            # Show the final buffed/debuffed score
            final_val = self.model.get_final_ability_score(self.ability_name)
            self.score_field.value = str(final_val)

        # Update Checkboxes based on mode
        for checkbox in self.skill_checkboxes:
            checkbox.disabled = not is_edit
            skill_name = checkbox.data["skill"]
            
            if is_edit:
                checkbox.value = self.model.ability_scores[self.ability_name]["skills"][skill_name]["base_proficient"]
            else:
                checkbox.value = self.model.is_skill_proficient(self.ability_name, skill_name)

        if self.page:
            self.update()