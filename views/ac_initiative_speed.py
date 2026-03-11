import flet as ft
from models.character_model import CharacterModel

class AcInitiativeSpeed(ft.Container):
    def __init__(self, model: CharacterModel, on_change_handler):
        super().__init__(
            padding=10,
            bgcolor=ft.Colors.RED_200,
            border=ft.border.all(2, ft.Colors.OUTLINE),
            border_radius=8
        )
        
        self.on_header_change = on_change_handler

        # --- 1. Define the UI Controls ---
        # Make derived stats read_only so the user cannot manually edit them
        self.armor_class = ft.TextField(label="Armor Class", value=str(model.armor_class), read_only=True, col={"sm": 12, "md": 4})
        
        # Format initiative to show a + if positive
        init_str = f"+{model.initiative}" if model.initiative >= 0 else str(model.initiative)
        self.initiative = ft.TextField(label="Initiative", value=init_str, read_only=True, col={"sm": 12, "md": 4})
        
        # Speed can still be editable (or you can derive it from Race later!)
        self.speed = ft.TextField(label="Speed", value=str(model.speed), data="speed", on_change=self.on_header_change, col={"sm": 12, "md": 4})

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