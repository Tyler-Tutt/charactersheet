import flet as ft
from typing import TYPE_CHECKING
from models.character_model import CharacterModel
if TYPE_CHECKING:
    from controllers.character_sheet_controller import CharacterSheetController


class AcInitiativeSpeed(ft.Container):
    '''
    Contains Armor Class, Initiative, and Speed fields
    '''
    def __init__(self, model: CharacterModel, controller: 'CharacterSheetController'):
        super().__init__(
            padding=10,
            bgcolor=ft.Colors.RED_200,
            border=ft.border.all(2, ft.Colors.OUTLINE),
            border_radius=8
        )
        
        self.controller = controller

        # --- 1. Define the UI Controls ---
        self.armor_class = ft.TextField(label="Armor Class", value=str(model.armor_class), read_only=True, col={"sm": 12, "md": 4})
        # Format initiative to show a + if positive
        initiative_string = f"+{model.initiative}" if model.initiative >= 0 else str(model.initiative)
        self.initiative = ft.TextField(label="Initiative", value=initiative_string, read_only=True, col={"sm": 12, "md": 4})
        
        # Speed can still be editable (or you can derive it from Race later!)
        self.speed = ft.TextField(label="Speed", value=str(model.speed), data="speed", on_change=self.controller.handle_header_change, col={"sm": 12, "md": 4})

        # --- 2. Build the Layout ---
        self.content = ft.ResponsiveRow(
            controls=[
                self.armor_class,
                self.initiative,
                self.speed,
            ]
        )

    def update_stats_data(self, model: CharacterModel):
        """Called by the main controller to refresh UI from the Model."""
        self.armor_class.value = str(model.armor_class)
        
        init_str = f"+{model.initiative}" if model.initiative >= 0 else str(model.initiative)
        self.initiative.value = init_str
        
        self.speed.value = str(model.speed)
        
        # Tell Flet to redraw ONLY this card
        self.update()