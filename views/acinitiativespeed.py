import flet as ft
from models.character_model import CharacterModel

class AcInitiativeSpeed(ft.Container):
    def __init__(self, model: CharacterModel, on_change_handler):
        # Initialize the parent Container
        super().__init__(
            padding=10,
            bgcolor=ft.Colors.RED_200,
            border=ft.border.all(2, ft.Colors.OUTLINE),
            border_radius=8
        )
        
        self.on_header_change = on_change_handler

        # --- 1. Define the UI Controls ---
        self.armor_class = ft.TextField(label="Armor Class", value=model.armor_class, data="armor_class", expand=True, on_change=self.on_header_change)
        self.initiative = ft.TextField(label="Initiative", value=model.initiative, data="initiative", expand=True, on_change=self.on_header_change)
        self.speed = ft.TextField(label="Speed", value=model.speed, data="speed", expand=True, on_change=self.on_header_change)

        # --- 2. Build the Layout ---
        self.content = ft.Row(
            controls=[
                ft.Container(
                    expand=1,
                    bgcolor=ft.Colors.AMBER_900,
                    padding=5,
                    border_radius=5,
                    content=ft.Row(
                        controls=[
                            self.armor_class,
                            self.initiative,
                            self.speed,
                        ]
                    ),
                ),
            ]
        )

    def update_stats_data(self, model: CharacterModel):
        """Called by the main controller when loading a character."""
        self.armor_class.value = str(model.armor_class)
        self.initiative.value = str(model.max_hp)
        self.speed.value = str(model.speed)
        
        # Tell Flet to redraw ONLY this card
        self.update()