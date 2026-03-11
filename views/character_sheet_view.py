import flet as ft
from models.character_model import CharacterModel
from views.ability_score_container import AbilityScoreContainer
from views.character_header_container import CharacterHeaderContainer
from views.ac_initiative_speed import AcInitiativeSpeed

class CharacterSheetView(ft.Container):
    def __init__(self, model: CharacterModel, on_score_change_handler, on_header_change_handler, on_skill_prof_change_handler):
        super().__init__(expand=True)
        self.model = model
        
        self.on_score_change = on_score_change_handler
        self.on_header_change = on_header_change_handler
        self.on_skill_prof_change = on_skill_prof_change_handler

        self.ability_score_containers = []
        self.content = self.build_ui()

    def build_ui(self):
        self.header = CharacterHeaderContainer(self.model, self.on_header_change)
        self.achpspeed = AcInitiativeSpeed(self.model, self.on_header_change)
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
                        controls=[*self.ability_score_containers]
                    ),
                    ft.Column(
                        col={"sm": 12, "md": 4},
                        controls=[self.achpspeed]
                    ),
                    ft.Column(
                        col={"sm": 12, "md": 4},
                        controls=[ft.Text("Features & Traits")]
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
                on_score_change=self.on_score_change,
                on_skill_prof_change=self.on_skill_prof_change
            )
            containers.append(card)
        return containers