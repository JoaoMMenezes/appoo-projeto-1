import flet as ft

def grades(page: ft.Page):
    return ft.Column(
        route="/notas",
        controls=[
            ft.Text("Notas", size=24),
            ft.Text("Matemática: 8.5"),
            ft.Text("História: 9.0"),
            ft.Text("Física: 7.5"),
            ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/home"))
        ]
    )