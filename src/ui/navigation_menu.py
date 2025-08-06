import flet as ft

try:
    from .theme.spacing import SPACE_2, SPACE_3
    from .theme import colors
except Exception:  # pragma: no cover
    from theme.spacing import SPACE_2, SPACE_3
    from theme import colors

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
        self.border_radius = 8
        self.content = ft.Row(
            [ft.Icon(destination.icon), ft.Text(destination.label)],
            spacing=SPACE_2,
        )
        self.on_click = item_clicked

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
        for item in self.controls:
            item.bgcolor = None
            item.content.controls[0].name = item.destination.icon
        sel = self.controls[self.selected_index]
        sel.bgcolor = colors.SECONDARY_CONTAINER
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
        self.padding = 0
        self.spacing = SPACE_3
        self.controls = [self.rail]

    def update_layout(self, width: int):
        self.rail.update_layout(width)
