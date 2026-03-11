import flet as ft
from models.character_model import CharacterModel

class AcInitiativeSpeed(ft.Container):
    '''
    ft.Container containing AC, Initiative, & Speed Fields.
    Also containting the function to handle loading this data from the model when loading a character.
    '''
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
        self.armor_class = ft.TextField(label="Armor Class", value=model.armor_class, data="armor_class", on_change=self.on_header_change, col={"sm": 12, "md": 4})
        self.initiative = ft.TextField(label="Initiative", value=model.initiative, data="initiative", on_change=self.on_header_change, col={"sm": 12, "md": 4})
        self.speed = ft.TextField(label="Speed", value=model.speed, data="speed", on_change=self.on_header_change, col={"sm": 12, "md": 4})

        # --- 2. Build the Layout ---
        self.content = ft.ResponsiveRow(
            controls=[
                self.armor_class,
                self.initiative,
                self.speed,
            ]
        )

    def load_acinitiativespeed_data(self, model: CharacterModel):
        """Called by the main controller when loading a character."""
        self.armor_class.value = str(model.armor_class)
        self.initiative.value = str(model.initiative)
        self.speed.value = str(model.speed)
        
        # Tell Flet to redraw ONLY this card
        self.update()