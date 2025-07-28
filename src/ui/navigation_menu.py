import flet as ft

try:
    from .tokens import SPACE_2, SPACE_3, SPACE_5
except Exception:  # pragma: no cover
    from tokens import SPACE_2, SPACE_3, SPACE_5

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
        self.content = ft.Row(
            [ft.Icon(destination.icon), ft.Text(destination.label)],
            spacing=SPACE_2,
        )
        self.on_click = item_clicked

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
        for item in self.controls:
            item.bgcolor = None
            item.content.controls[0].name = item.destination.icon
        sel = self.controls[self.selected_index]
        sel.bgcolor = ft.colors.SECONDARY_CONTAINER
        sel.content.controls[0].name = sel.destination.selected_icon

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
        self.padding = SPACE_5
        self.spacing = SPACE_3
        self.controls = [
            self.rail,
            ft.Column(
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
                padding=ft.padding.only(top=SPACE_5),
            ),
        ]

    def theme_changed(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.dark_light_text.value = "Dark theme"
            self.dark_light_icon.icon = ft.icons.BRIGHTNESS_HIGH
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.dark_light_text.value = "Light theme"
            self.dark_light_icon.icon = ft.icons.BRIGHTNESS_2
        self.page.update()
