import flet as ft


def layout(page: ft.Page, conteudo, titulo: str, index_ativo: int):
    return ft.View(
        route="/",
        controls=[
            ft.Row([
                ft.NavigationRail(
                    selected_index=index_ativo,
                    label_type=ft.NavigationRailLabelType.ALL,
                    destinations=[
                        ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Início"),
                        ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Perfil"),
                        ft.NavigationRailDestination(icon=ft.Icons.SCHOOL, label="Notas"),
                    ],
                    on_change=lambda e: page.go(["/home", "/perfil", "/notas"][e.control.selected_index]),
                    height=page.window.height - 50,
                    width=page.window.width * 0.15,
                    elevation=3,
                ),
                ft.VerticalDivider(width=1),
                ft.Column([
                    ft.Text(titulo, size=24, weight="bold"),
                    conteudo,
                    ft.ElevatedButton("Sair", on_click=lambda e: page.go("/")),
                ], expand=True, spacing=20)
            ], expand=True)
        ]
    )
