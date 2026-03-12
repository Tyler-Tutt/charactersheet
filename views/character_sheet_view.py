import flet as ft
from models.character_model import CharacterModel
from views.components.ability_score_container import AbilityScoreContainer
from views.components.character_header_container import CharacterHeaderContainer
from views.components.ac_initiative_speed_container import AcInitiativeSpeed

class CharacterSheetView(ft.Container):
    def __init__(self, model: CharacterModel, controller):
        super().__init__(expand=True)
        self.model = model
        self.controller = controller
        self.ability_score_containers = []
        self.content = self.build_ui()

    def build_ui(self):
        '''
        Assembles child rows, columns, and containers
        '''
        self.header = CharacterHeaderContainer(self.model, self.controller)
        self.achpspeed = AcInitiativeSpeed(self.model, self.controller)
        self.proficiency_bonus_field = ft.TextField(
            label="Proficiency Bonus",
            value=self.model.format_modifier(self.model.proficiency_bonus),
            read_only=True,
            text_align=ft.TextAlign.CENTER,
            # weight=ft.FontWeight.BOLD,
        )
        self.second_row_container = self._create_row_2()
        
        return ft.Column(
            controls=[
                self.header,
                ft.Divider(height=20),
                self.second_row_container,
            ]
        )

    def _create_row_2(self):
        self.ability_score_containers = self._create_ability_score_containers()
        return ft.Container(
            bgcolor=ft.Colors.LIGHT_BLUE,
            border=ft.border.all(2),
            padding=5,
            content=ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        col={"sm": 12, "md": 4},
                        controls=[
                            self.proficiency_bonus_field,
                            *self.ability_score_containers
                            ]
                    ),
                    ft.Column(
                        col={"sm": 12, "md": 4},
                        controls=[
                            self.achpspeed
                            ]
                    ),
                    ft.Column(
                        col={"sm": 12, "md": 4},
                        controls=[
                            ft.Text("Features & Traits")
                            ]
                    )
                ]
            )
        )

    def _create_ability_score_containers(self):
        containers = []
        for ability_name in self.model.abilities_list:
            card = AbilityScoreContainer(
                model=self.model,
                ability_name=ability_name,
                controller=self.controller
            )
            containers.append(card)
        return containers
    
    def update_proficiency_bonus(self):
        """Pulls fresh Proficiency Bonus from the Model and updates the UI."""
        self.proficiency_bonus_field.value = self.model.format_modifier(self.model.proficiency_bonus)
        self.proficiency_bonus_field.update()