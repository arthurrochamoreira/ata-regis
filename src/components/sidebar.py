"""Sidebar component with navigation and theme controls."""
import flet as ft
from ..constants import SPACE_3, SPACE_4, SPACE_5


def create_sidebar(app) -> ft.Container:
    """Return sidebar container."""
    def nav_click(view: str):
        app.current_view = view
        app.render_view()
        app.page.update()

    theme_button = ft.IconButton(
        icon=ft.icons.BRIGHTNESS_6,
        tooltip="Alternar tema",
        on_click=app.toggle_theme,
    )

    color_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("BLUE"),
            ft.dropdown.Option("GREEN"),
            ft.dropdown.Option("INDIGO"),
        ],
        value="BLUE",
        on_change=lambda e: app.change_primary_color(e.control.value),
        dense=True,
        visible=app.is_sidebar_open,
    )
    app.color_dropdown = color_dropdown

    items = [
        ("Dashboard", ft.icons.HOME, "dashboard"),
        ("Atas", ft.icons.LIST_ALT, "atas"),
        ("Vencimentos", ft.icons.SCHEDULE, "vencimentos"),
    ]

    def build_item(label, icon, view):
        return ft.Container(
            content=ft.Row(
                [ft.Icon(icon), ft.Text(label, visible=app.is_sidebar_open)],
                spacing=SPACE_3,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(vertical=SPACE_3, horizontal=SPACE_4),
            on_click=lambda e: nav_click(view),
        )

    nav_controls = [build_item(*item) for item in items]

    footer = ft.Row(
        [theme_button, color_dropdown],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=SPACE_4,
    )

    sidebar = ft.Container(
        width=250 if app.is_sidebar_open else 70,
        bgcolor=ft.colors.SURFACE_VARIANT,
        content=ft.Column(nav_controls + [ft.Container(expand=True), footer], spacing=SPACE_5, expand=True),
    )
    return sidebar
