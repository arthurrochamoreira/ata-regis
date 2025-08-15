import json
import math
import flet as ft

from .theme.spacing import SPACE_2, SPACE_3, SPACE_4, SPACE_5, SPACE_6
from .theme.shadows import SHADOW_XL
from .theme import colors


class NavigationDestination:
    def __init__(self, name: str, label: str, icon: str, selected_icon: str, index: int):
        self.name = name
        self.label = label
        self.icon = icon
        self.selected_icon = selected_icon
        self.index = index


class SidebarItem(ft.TextButton):
    def __init__(self, destination: NavigationDestination, activate_cb, duration: int, curve: str):
        super().__init__()
        self.destination = destination
        self.activate_cb = activate_cb
        self.tab_index = 0
        self.icon = ft.Icon(destination.icon)
        self.label = ft.Text(destination.label)
        self.label_container = ft.Container(
            content=self.label,
            opacity=1,
            animate=ft.animation.Animation(duration, curve),
        )
        self.content = ft.Row(
            [self.icon, self.label_container],
            spacing=SPACE_2,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.expand = True
        self.style = ft.ButtonStyle(
            padding=ft.padding.all(SPACE_3),
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.with_opacity(0.05, ft.colors.BLACK),
                ft.MaterialState.FOCUSED: ft.colors.with_opacity(0.08, ft.colors.BLACK),
            },
            overlay_color={ft.MaterialState.FOCUSED: ft.colors.with_opacity(0.08, ft.colors.BLACK)},
        )
        self.on_click = self.on_pressed

    def on_pressed(self, e):
        self.activate_cb(self.destination.index)

    def set_collapsed(self, collapsed: bool):
        self.label_container.width = 0 if collapsed else None
        self.label_container.opacity = 0 if collapsed else 1
        self.content.alignment = ft.MainAxisAlignment.CENTER if collapsed else ft.MainAxisAlignment.START
        self.tooltip = self.destination.label if collapsed else None

    def set_active(self, active: bool):
        self.icon.name = self.destination.selected_icon if active else self.destination.icon
        self.style = ft.ButtonStyle(
            padding=ft.padding.all(SPACE_3),
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor={
                ft.MaterialState.DEFAULT: ft.colors.SECONDARY_CONTAINER if active else None,
                ft.MaterialState.HOVERED: ft.colors.with_opacity(0.05, ft.colors.BLACK),
                ft.MaterialState.FOCUSED: ft.colors.with_opacity(0.08, ft.colors.BLACK),
            },
            overlay_color={ft.MaterialState.FOCUSED: ft.colors.with_opacity(0.08, ft.colors.BLACK)},
        )


class Sidebar(ft.Container):
    def __init__(self, app, open_width: int = 240, closed_width: int = 68, duration: int = 300, curve: str = "ease"):
        self.app = app
        self.open_width = open_width
        self.closed_width = closed_width
        self.duration = duration
        self.curve = curve
        self.collapsed = False

        self.destinations = [
            NavigationDestination("dashboard", "Dashboard", ft.icons.INSIGHTS_OUTLINED, ft.icons.INSIGHTS, 0),
            NavigationDestination("atas", "Atas", ft.icons.LIST_OUTLINED, ft.icons.LIST, 1),
            NavigationDestination("vencimentos", "Vencimentos", ft.icons.ALARM_OUTLINED, ft.icons.ALARM, 2),
            NavigationDestination("config", "Configurações", ft.icons.SETTINGS_OUTLINED, ft.icons.SETTINGS, 3),
        ]

        self.items: list[SidebarItem] = []
        nav_items: list[ft.Control] = []
        for d in self.destinations:
            nav_items.append(self.render_sidebar_item(d.icon, d.label, d.name, d.index == self.app.current_tab))

        self.toggle_btn = ft.IconButton(
            icon=ft.icons.MENU_OUTLINED,
            tooltip="Colapsar menu",
            on_click=self.toggle_sidebar,
            rotate=ft.transform.Rotate(0),
            animate_rotation=ft.animation.Animation(duration, curve),
        )
        self.toggle_btn.aria_label = "Colapsar menu"

        self.logo = ft.Icon(ft.icons.DESCRIPTION_OUTLINED)
        self.title = ft.Text("Ata RP")
        self.title_container = ft.Container(
            content=self.title,
            opacity=1,
            animate=ft.animation.Animation(duration, curve),
        )
        left_header = ft.Row(
            [self.logo, self.title_container],
            spacing=SPACE_2,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        header_row = ft.Row(
            [left_header, self.toggle_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.header = ft.Container(
            content=header_row,
            padding=ft.padding.symmetric(horizontal=SPACE_5, vertical=SPACE_4),
        )

        self.nav = ft.Container(
            content=ft.Column(nav_items, spacing=SPACE_3, expand=True),
            padding=ft.padding.symmetric(horizontal=SPACE_5, vertical=SPACE_3),
            expand=True,
        )

        theme_btn = ft.IconButton(
            icon=ft.icons.BRIGHTNESS_6_OUTLINED,
            tooltip="Alternar tema",
            on_click=self.app.toggle_theme if hasattr(self.app, "toggle_theme") else None,
        )
        self.footer = ft.Container(
            content=ft.Row([theme_btn], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=SPACE_3, horizontal=SPACE_5),
            margin=ft.margin.only(top=SPACE_6),
        )

        content = ft.Column([
            self.header,
            self.nav,
            self.footer,
        ], spacing=0, expand=True)

        super().__init__(
            content=content,
            width=open_width,
            bgcolor=colors.WHITE,
            shadow=SHADOW_XL,
            animate=ft.animation.Animation(duration, curve),
        )

        self.update_selected_item()
        self.restore_state()

    def render_sidebar_item(self, icon, label, route, active: bool):
        selected_icon = next(
            (d.selected_icon for d in self.destinations if d.name == route),
            icon,
        )
        dest = NavigationDestination(route, label, icon, selected_icon, len(self.items))
        item = SidebarItem(dest, activate_cb=self.item_clicked, duration=self.duration, curve=self.curve)
        item.set_collapsed(False)
        item.set_active(active)
        self.items.append(item)
        return item

    def item_clicked(self, index: int):
        self.selected_index = index
        self.update_selected_item()
        self.app.navigate_to(index)

    def update_selected_item(self):
        for item in self.items:
            item.set_active(item.destination.index == getattr(self, "selected_index", self.app.current_tab))

    def toggle_sidebar(self, e=None):
        self.set_collapsed(not self.collapsed)

    def set_collapsed(self, value: bool):
        self.collapsed = value
        self.width = self.closed_width if value else self.open_width
        self.toggle_btn.rotate.angle = math.pi if value else 0
        label = "Expandir menu" if value else "Colapsar menu"
        self.toggle_btn.tooltip = label
        self.toggle_btn.aria_label = label
        self.title_container.width = 0 if value else None
        self.title_container.opacity = 0 if value else 1
        for item in self.items:
            item.set_collapsed(value)
        self.app.page.client_storage.set("sidebar_collapsed", json.dumps(value))
        print("sidebar_collapsed" if value else "sidebar_expanded")
        if self.page:
            self.update()

    def restore_state(self):
        stored = self.app.page.client_storage.get("sidebar_collapsed")
        if stored is not None:
            value = json.loads(stored)
        else:
            value = self.app.page.width < 768
        self.set_collapsed(value)

    def update_layout(self, width: int):
        if width < 768 and not self.collapsed:
            self.set_collapsed(True)
