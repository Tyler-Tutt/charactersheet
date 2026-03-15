import flet as ft
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.character_model import CharacterModel
    from controllers.character_sheet_controller import CharacterSheetController

class InventoryContainer(ft.Container):
    '''
    A ft.Container that contains a list of the Character's Items
    '''
    def __init__(self, model: 'CharacterModel', controller: 'CharacterSheetController'):
        super().__init__(
            padding=10,
            bgcolor=ft.Colors.GREY_800,
            border=ft.border.all(2, ft.Colors.OUTLINE),
            border_radius=8
        )
        self.model = model
        self.controller = controller
        
        self.item_list_column = ft.Column()
        
        # A test button to add our Cloak
        self.add_test_item_btn = ft.ElevatedButton(
            text="Loot 'Cloak of Protection'", 
            on_click=lambda _: self.controller.add_item_to_inventory("Cloak of Protection")
        )

        self.content = ft.Column(
            controls=[
                ft.Text("Inventory & Attunement", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                self.add_test_item_btn,
                ft.Divider(),
                self.item_list_column
            ]
        )
        
        self.update_inventory_ui()

    def update_inventory_ui(self):
        """Redraws the list of inventory items based on the model."""
        self.item_list_column.controls.clear()
        
        for index, item in enumerate(self.model.inventory):
            # Create a row for each item
            item_row = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(item.name, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500, expand=True),
                    ft.Text(item.description, color=ft.Colors.GREY_400, size=12, expand=True),
                    ft.Checkbox(
                        label="Attuned", 
                        value=item.is_equipped, 
                        data=index, # Pass the index so the controller knows WHICH item
                        on_change=self.controller.toggle_item_attunement
                    )
                ]
            )
            self.item_list_column.controls.append(item_row)
            
        if self.page:
            self.update()
            
    def set_edit_mode(self, is_edit: bool):
        # Optional: Hide the add button if not in edit mode
        self.add_test_item_btn.visible = is_edit
        if self.page:
            self.update()