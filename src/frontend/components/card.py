import flet as ft

def criar_cartao(titulo: str, subtitulo: str):
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text(titulo, size=18, weight="bold"),
                ft.Text(subtitulo, size=14, color=ft.Colors.GREY_700),
            ]),
            padding=15,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
        ),
        elevation=3,
    )