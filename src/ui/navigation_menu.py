import flet as ft

try:
    from .theme.spacing import SPACE_2, SPACE_3, SPACE_4, SPACE_5
    from .theme import colors as theme_colors
except Exception:  # pragma: no cover
    from theme.spacing import SPACE_2, SPACE_3, SPACE_4, SPACE_5
    from theme import colors as theme_colors

class PopupColorItem(ft.PopupMenuItem):
    def __init__(self, color: str, name: str):
        super().__init__()
        self.content = ft.Row(
            controls=[ft.Icon(name=ft.icons.COLOR_LENS_OUTLINED, color=color), ft.Text(name)]
        )
        self.data = color
        self.on_click = self.seed_color_changed

    def seed_color_changed(self, e):
        self.page.theme = self.page.dark_theme = ft.Theme(color_scheme_seed=self.data)
        self.page.update()

class NavigationDestination:
    def __init__(self, name: str, label: str, icon: str, selected_icon: str, index: int):
        self.name = name
        self.label = label
        self.icon = icon
        self.selected_icon = selected_icon
        self.index = index

class NavigationItem(ft.Container):
    def __init__(self, destination: NavigationDestination, item_clicked):
        super().__init__()
        self.destination = destination
        self.ink = True
        self.padding = SPACE_3
        self.border_radius = 5
        self.selected = False
        self.icon = ft.Icon(destination.icon)
        self.label = ft.Text(destination.label)
        self.content = ft.Row([self.icon, self.label], spacing=SPACE_2)
        self.on_click = item_clicked
        self.on_hover = self.handle_hover
        self.apply_theme()

    def handle_hover(self, e: ft.HoverEvent):
        scheme = theme_colors.scheme(self.page)
        if e.data == "true":
            self.bgcolor = scheme["nav_link_hover_bg"]
            color = scheme["nav_link_hover_text"]
            self.icon.color = color
            self.label.color = color
        else:
            self.apply_theme()
        self.update()

    def apply_theme(self):
        scheme = theme_colors.scheme(self.page)
        if self.selected:
            self.bgcolor = scheme["nav_link_active_bg"]
            color = scheme["nav_link_active_text"]
        else:
            self.bgcolor = None
            color = scheme["nav_link"]
        self.icon.color = color
        self.label.color = color

    def set_collapsed(self, collapsed: bool):
        """Show only icon when collapsed"""
        self.content.controls[1].visible = not collapsed
        self.padding = ft.padding.all(SPACE_2 if collapsed else SPACE_3)
        self.width = None

class NavigationColumn(ft.Column):
    def __init__(self, app, destinations: list[NavigationDestination]):
        super().__init__()
        self.app = app
        self.destinations = destinations
        self.selected_index = app.current_tab
        self.expand = 4
        self.spacing = 0
        self.scroll = ft.ScrollMode.ALWAYS
        self.width = 200
        self.controls = self.get_navigation_items()

    def update_layout(self, width: int):
        collapsed = width < 1024
        self.width = 60 if collapsed else 200
        for item in self.controls:
            item.set_collapsed(collapsed)

    def before_update(self):
        super().before_update()
        self.update_selected_item()

    def get_navigation_items(self):
        items = []
        for d in self.destinations:
            items.append(NavigationItem(d, item_clicked=self.item_clicked))
        return items

    def item_clicked(self, e):
        self.selected_index = e.control.destination.index
        self.update_selected_item()
        self.app.navigate_to(self.selected_index)

    def update_selected_item(self):
        for index, item in enumerate(self.controls):
            item.selected = index == self.selected_index
            item.icon.name = item.destination.selected_icon if item.selected else item.destination.icon
            item.apply_theme()

    def apply_theme(self):
        for item in self.controls:
            item.apply_theme()

class LeftNavigationMenu(ft.Column):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.destinations = [
            NavigationDestination("dashboard", "Dashboard", ft.icons.INSIGHTS_OUTLINED, ft.icons.INSIGHTS, 0),
            NavigationDestination("atas", "Atas", ft.icons.LIST_OUTLINED, ft.icons.LIST, 1),
            NavigationDestination("vencimentos", "Vencimentos", ft.icons.ALARM_OUTLINED, ft.icons.ALARM, 2),
        ]
        self.rail = NavigationColumn(app, self.destinations)
        self.dark_light_text = ft.Text("Light theme")
        self.dark_light_icon = ft.IconButton(icon=ft.icons.BRIGHTNESS_2_OUTLINED, tooltip="Toggle brightness", on_click=self.theme_changed)
        self.padding = 0
        self.spacing = SPACE_3
        self.controls = [
            self.rail,
            ft.Container(
                padding=ft.padding.only(top=SPACE_5),
                content=ft.Column(
                    expand=1,
                    spacing=SPACE_3,
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Row([self.dark_light_icon, self.dark_light_text], spacing=SPACE_2),
                        ft.Row([
                            ft.PopupMenuButton(
                                icon=ft.icons.COLOR_LENS_OUTLINED,
                                items=[
                                    PopupColorItem(color="deeppurple", name="Deep purple"),
                                    PopupColorItem(color="indigo", name="Indigo"),
                                    PopupColorItem(color="blue", name="Blue"),
                                    PopupColorItem(color="teal", name="Teal"),
                                    PopupColorItem(color="green", name="Green"),
                                    PopupColorItem(color="yellow", name="Yellow"),
                                    PopupColorItem(color="orange", name="Orange"),
                                    PopupColorItem(color="deeporange", name="Deep orange"),
                                    PopupColorItem(color="pink", name="Pink"),
                                ],
                            ),
                            ft.Text("Seed color"),
                        ], spacing=SPACE_2)
                    ],
                ),
            ),
        ]
        self.refresh_theme()

    def theme_changed(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.dark_light_text.value = "Dark theme"
            self.dark_light_icon.icon = ft.icons.BRIGHTNESS_HIGH
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.dark_light_text.value = "Light theme"
            self.dark_light_icon.icon = ft.icons.BRIGHTNESS_2
        self.app.apply_theme()
        self.app.refresh_ui()

    def update_layout(self, width: int):
        self.rail.update_layout(width)

    def refresh_theme(self):
        """Apply theme colors to navigation menu."""
        scheme = theme_colors.scheme(self.page)
        self.dark_light_text.color = scheme["nav_link"]
        self.dark_light_icon.icon_color = (
            scheme["toggle_moon"] if self.page.theme_mode == ft.ThemeMode.LIGHT else scheme["toggle_sun"]
        )
        self.rail.apply_theme()
