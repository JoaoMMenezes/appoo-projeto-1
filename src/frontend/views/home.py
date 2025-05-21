import flet as ft
from components.card import criar_cartao

def home(page: ft.Page):
    tipo_usuario = page.client_storage.get("tipo_usuario")

    aulas = [
        ("Matemática", "08:00 - Sala 101"),
        ("História", "10:00 - Sala 202"),
        ("Física", "14:00 - Laboratório"),
    ] if tipo_usuario == "aluno" else [
        ("Biologia", "09:00 - Sala 105"),
        ("Química", "13:00 - Sala 201"),
    ]

    return ft.Column(
        route="/home",
        controls=[_layout_nav(page, 0, "Início", aulas)]
    )

def _layout_nav(page, index, titulo, dados):
    return ft.Row([
        _nav_rail(page, index),
        ft.VerticalDivider(width=1),
        ft.Column([
            ft.Text(titulo, size=24, weight="bold"),
            ft.Column([criar_cartao(d, h) for d, h in dados], scroll=ft.ScrollMode.AUTO, spacing=10),
            ft.ElevatedButton("Sair", on_click=lambda _: page.go("/"))
        ])
    ], expand=True)

def _nav_rail(page, index):
    return ft.NavigationRail(
        selected_index=index,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Início"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Perfil"),
            ft.NavigationRailDestination(icon=ft.Icons.SCHOOL, label="Notas"),
        ],
        on_change=lambda e: page.go(["/home", "/perfil", "/notas"][e.control.selected_index]),
        height=page.window.height - 50,
        width=60
    )