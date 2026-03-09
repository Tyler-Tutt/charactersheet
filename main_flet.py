import flet as ft
from controllers.character_controller import CharacterController
import database

def main(page: ft.Page):
    # --- Page Setup ---
    page.title = "Flet Character Sheet"
    page.scroll = ft.ScrollMode.AUTO
    
    # --- Initialize Controller ---
    # The controller handles creating the model and the view
    app_controller = CharacterController(page)

    # --- Menu / AppBar ---
    # Notice we pass the controller's methods to the buttons
    page.appbar = ft.AppBar(
        title=ft.Text("Flet Character Sheet"),
        actions=[
            ft.IconButton(
                ft.Icons.SAVE, 
                on_click=app_controller.save_character, 
                tooltip="Save Character"
            ),
            ft.IconButton(
                ft.Icons.FOLDER_OPEN, 
                on_click=app_controller.open_load_dialog, 
                tooltip="Load Character"
            ),
        ]
    )

    # --- Add View to Page ---
    page.add(app_controller.get_view())
    page.update()

if __name__ == "__main__":
    database.init_db()
    ft.app(target=main)