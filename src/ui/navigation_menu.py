import flet as ft

try:
    from ui.theme import Theme
except ImportError:  # pragma: no cover - package relative import
    from .theme import Theme


class MenuItem(ft.Container):
    """Single entry in the sidebar."""

    def __init__(self, app, index: int, label: str, icon: str):
        active = app.current_tab == index
        super().__init__(
            bgcolor=Theme.GREY if active else Theme.LIGHT,
            border_radius=ft.border_radius.only(top_left=48, bottom_left=48),
            padding=4,
            content=ft.Row(
                controls=[
                    ft.Icon(name=icon, color=Theme.BLUE if active else Theme.DARK),
                    ft.Text(label, visible=not getattr(app.page, "drawer_open", False)),
                ],
                vertical_alignment="center",
            ),
            on_click=lambda e: app.navigate_to(index),
        )


class LeftNavigationMenu(ft.Container):
    """Sidebar navigation similar to the provided dashboard example."""

    def __init__(self, app):
        super().__init__(width=280, bgcolor=Theme.LIGHT)
        self.app = app
        self.update_menu()

    def update_menu(self):
        items = [
            ("Dashboard", ft.icons.DASHBOARD_OUTLINED),
            ("Atas", ft.icons.LIBRARY_BOOKS_OUTLINED),
            ("Vencimentos", ft.icons.ALARM_OUTLINED),
        ]
        menu_items = [MenuItem(self.app, i, label, icon) for i, (label, icon) in enumerate(items)]
        menu_items.append(ft.Expander(visible=False))
        menu_items.append(
            ft.Container(
                padding=ft.Padding(12, 4),
                content=ft.Row(
                    [ft.Icon(ft.icons.LOGOUT, color=Theme.RED), ft.Text("Sair", color=Theme.RED)],
                    vertical_alignment="center",
                ),
            )
        )
        self.content = ft.Column(controls=menu_items, spacing=10, scroll="adaptive")
