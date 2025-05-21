import flet as ft

def profile(page: ft.Page):
    return ft.Column(
        route="/perfil",
        controls=[
            ft.Text("Perfil do Usuário", size=24),
            ft.Text("Nome: João da Silva"),
            ft.Text("Curso: Engenharia da Computação"),
            ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/home"))
        ]
    )