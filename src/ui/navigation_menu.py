import flet as ft

try:
    from .theme.spacing import SPACE_2, SPACE_3, SPACE_4, SPACE_5
except Exception:  # pragma: no cover
    from theme.spacing import SPACE_2, SPACE_3, SPACE_4, SPACE_5

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
    def __init__(self, destination: NavigationDestination, item_clicked, theme):
        super().__init__()
        self.destination = destination
        self.theme = theme
        self.selected = False
        self.ink = True
        self.padding = SPACE_3
        self.border_radius = 8
        link_color = theme["sidebar"]["link"]
        self.content = ft.Row(
            [
                ft.Icon(destination.icon, color=link_color),
                ft.Text(destination.label, color=link_color),
            ],
            spacing=SPACE_2,
        )
        # Store destination index in `data` so it is preserved in events
        self.data = destination.index
        self.on_click = item_clicked
        self.on_hover = self.hovered

    def hovered(self, e):
        if self.selected:
            return
        if e.data == "true":
            self.bgcolor = self.theme["sidebar"]["link_hover_bg"]
            color = self.theme["sidebar"]["link_hover_text"]
        else:
            self.bgcolor = None
            color = self.theme["sidebar"]["link"]
        self.content.controls[0].color = color
        self.content.controls[1].color = color
        if self.page:
            self.update()

    def set_selected(self, selected: bool):
        self.selected = selected
        if selected:
            self.bgcolor = self.theme["sidebar"]["link_active_bg"]
            color = self.theme["sidebar"]["link_active_text"]
        else:
            self.bgcolor = None
            color = self.theme["sidebar"]["link"]
        self.content.controls[0].color = color
        self.content.controls[1].color = color
        if self.page:
            self.update()

    def set_collapsed(self, collapsed: bool):
        """Show only icon when collapsed"""
        self.content.controls[1].visible = not collapsed
        self.padding = ft.padding.all(SPACE_2 if collapsed else SPACE_3)
        self.width = None

class NavigationColumn(ft.Column):
    def __init__(self, app, destinations: list[NavigationDestination], theme):
        super().__init__()
        self.app = app
        self.destinations = destinations
        self.selected_index = app.current_tab
        self.theme = theme
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
            items.append(NavigationItem(d, item_clicked=self.item_clicked, theme=self.theme))
        return items

    def item_clicked(self, e):
        # Retrieve index from control data set in NavigationItem
        self.selected_index = int(e.control.data)
        self.update_selected_item()
        if self.selected_index == 0:
            self.app.handle_dashboard_click(e)
        elif self.selected_index == 1:
            self.app.handle_atas_click(e)
        elif self.selected_index == 2:
            self.app.handle_vencimentos_click(e)

    def update_selected_item(self):
        for item in self.controls:
            item.set_selected(False)
            item.content.controls[0].name = item.destination.icon
        sel = self.controls[self.selected_index]
        sel.set_selected(True)
        sel.content.controls[0].name = sel.destination.selected_icon

class LeftNavigationMenu(ft.Column):
    def __init__(self, app, theme):
        super().__init__()
        self.app = app
        self.theme = theme
        self.destinations = [
            NavigationDestination("dashboard", "Dashboard", ft.icons.INSIGHTS_OUTLINED, ft.icons.INSIGHTS, 0),
            NavigationDestination("atas", "Atas", ft.icons.LIST_OUTLINED, ft.icons.LIST, 1),
            NavigationDestination("vencimentos", "Vencimentos", ft.icons.ALARM_OUTLINED, ft.icons.ALARM, 2),
        ]
        self.rail = NavigationColumn(app, self.destinations, theme)
        mode_text = "Light theme" if app.page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
        icon_color = (
            theme["sidebar"]["icon_moon"]
            if app.page.theme_mode == ft.ThemeMode.LIGHT
            else theme["sidebar"]["icon_sun"]
        )
        icon_name = (
            ft.icons.BRIGHTNESS_2_OUTLINED
            if app.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.icons.BRIGHTNESS_HIGH
        )
        self.dark_light_text = ft.Text(mode_text, color=theme["text"])
        self.dark_light_icon = ft.IconButton(
            icon=icon_name,
            tooltip="Toggle brightness",
            on_click=self.theme_changed,
            style=ft.ButtonStyle(
                bgcolor=theme["sidebar"]["toggle_bg"],
                color=icon_color,
            ),
        )
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
                            ft.Text("Seed color", color=theme["text"]),
                        ], spacing=SPACE_2)
                    ],
                ),
            ),
        ]

    def theme_changed(self, e):
        self.app.handle_theme_toggle(e)

    def update_layout(self, width: int):
        self.rail.update_layout(width)
