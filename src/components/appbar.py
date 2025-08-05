"""Top AppBar component."""
import flet as ft
from constants import SPACE_4


def create_appbar(app) -> ft.AppBar:
    """Return configured AppBar."""
    tools_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Verificar alertas", on_click=app.check_alerts),
            ft.PopupMenuItem(text="Gerar relatório", on_click=app.generate_report),
            ft.PopupMenuItem(text="Testar e-mail", on_click=app.test_email),
            ft.PopupMenuItem(text="Consultar status do sistema", on_click=app.check_system_status),
        ]
    )

    return ft.AppBar(
        title=ft.Text("Atas de Registro de Preços", weight=ft.FontWeight.BOLD),
        center_title=False,
        actions=[
            tools_menu,
            ft.ElevatedButton(
                "Nova Ata",
                icon=ft.icons.ADD,
                on_click=lambda e: app.open_new_ata_form(),
            ),
        ],
        bgcolor=ft.colors.SURFACE,
        elevation=2,
    )
