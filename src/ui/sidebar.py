import json
import math
import flet as ft

from .theme.spacing import SPACE_2, SPACE_3, SPACE_4, SPACE_5
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
        self.active = False

        self.icon = ft.Icon(destination.icon, color=colors.TEXT_SECONDARY)
        self.label = ft.Text(destination.label, color=colors.TEXT_PRIMARY)
        self.label_container = ft.Container(
            content=self.label,
            opacity=1,
            animate=ft.animation.Animation(duration, curve),
        )
        row = ft.Row(
            [self.icon, self.label_container],
            spacing=SPACE_2,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.inner_container = ft.Container(
            content=row,
            padding=ft.padding.symmetric(horizontal=SPACE_3, vertical=SPACE_3),
            border_radius=8,
        )
        self.content = self.inner_container
        self.style = ft.ButtonStyle(
            padding=0,
            bgcolor={ft.MaterialState.HOVERED: ft.colors.with_opacity(0.05, ft.colors.BLACK)},
            shape=ft.RoundedRectangleBorder(radius=8),
        )
        self.on_click = self.on_pressed
        self.on_hover = self._on_hover

    def on_pressed(self, e):
        self.activate_cb(self.destination.index)

    def set_collapsed(self, collapsed: bool):
        self.label_container.width = 0 if collapsed else None
        self.label_container.opacity = 0 if collapsed else 1
        self.tooltip = self.destination.label if collapsed else None

    def set_active(self, active: bool):
        self.active = active
        self.icon.name = self.destination.selected_icon if active else self.destination.icon
        self.icon.color = colors.PRIMARY if active else colors.TEXT_SECONDARY
        self.inner_container.bgcolor = ft.colors.with_opacity(0.08, colors.PRIMARY) if active else None
        self.inner_container.border = (
            ft.border.only(left=ft.BorderSide(width=3, color=colors.PRIMARY))
            if active
            else None
        )

    def _on_hover(self, e):
        hovered = e.data == "true"
        if hovered and not self.active:
            self.icon.color = colors.PRIMARY
        elif not self.active:
            self.icon.color = colors.TEXT_SECONDARY
        self.update()



class Sidebar(ft.Container):
    def __init__(self, app, open_width: int = 240, closed_width: int = 64, duration: int = 200, curve: str = "ease"):
        self.app = app
        self.open_width = open_width
        self.closed_width = closed_width
        self.duration = duration
        self.curve = curve
        self.sidebar_open = True
        self.destinations = [
            NavigationDestination("dashboard", "Dashboard", ft.icons.INSIGHTS_OUTLINED, ft.icons.INSIGHTS, 0),
            NavigationDestination("atas", "Atas", ft.icons.LIST_OUTLINED, ft.icons.LIST, 1),
            NavigationDestination("vencimentos", "Vencimentos", ft.icons.ALARM_OUTLINED, ft.icons.ALARM, 2),
        ]
        self.items: list[SidebarItem] = []

        # Header with menu icon and toggle arrow
        self.menu_icon = ft.Icon("side_navigation", color=colors.TEXT_PRIMARY)
        self.title = ft.Text("Menu", color=colors.TEXT_PRIMARY)
        self.title_container = ft.Container(
            content=self.title,
            opacity=1,
            animate=ft.animation.Animation(duration, curve),
        )
        self.toggle_btn = ft.IconButton(
            icon=ft.icons.CHEVRON_RIGHT,
            tooltip="Colapsar menu",
            on_click=self.toggle_sidebar,
            rotate=ft.transform.Rotate(0),
            animate_rotation=ft.animation.Animation(duration, curve),
        )
        self.toggle_btn.aria_label = "Colapsar menu"
        header_row = ft.Row(
            [self.menu_icon, self.title_container, self.toggle_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        header = ft.Container(
            content=header_row,
            padding=ft.padding.symmetric(horizontal=SPACE_3),
        )

        # Navigation items
        controls = []
        for d in self.destinations:
            controls.append(self.render_sidebar_item(d.icon, d.label, d.name, d.index == self.app.current_tab))

        content = ft.Column(
            [header, ft.Divider(height=1), *controls],
            spacing=SPACE_3,
            expand=True,
        )
        super().__init__(
            content=content,
            width=open_width,
            bgcolor=colors.CARD_BG,
            padding=ft.padding.symmetric(horizontal=SPACE_5, vertical=SPACE_4),
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
        self.set_sidebar_open(not self.sidebar_open)

    def set_sidebar_open(self, value: bool):
        self.sidebar_open = value
        self.width = self.open_width if value else self.closed_width
        self.toggle_btn.rotate.angle = 0 if value else math.pi
        label = "Colapsar menu" if value else "Expandir menu"
        self.toggle_btn.tooltip = label
        self.toggle_btn.aria_label = label
        self.title_container.width = None if value else 0
        self.title_container.opacity = 1 if value else 0
        for item in self.items:
            item.set_collapsed(not value)
        self.app.page.client_storage.set("sidebar_open", json.dumps(value))
        print("sidebar_opened" if value else "sidebar_closed")
        if self.page:
            self.update()

    def restore_state(self):
        stored = self.app.page.client_storage.get("sidebar_open")
        if stored is not None:
            value = json.loads(stored)
        else:
            value = self.app.page.width >= 768
        self.set_sidebar_open(value)

    def update_layout(self, width: int):
        if width < 768 and self.sidebar_open:
            self.set_sidebar_open(False)
