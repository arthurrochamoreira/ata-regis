import json
import math
from typing import Callable, List, Optional

import flet as ft

from .theme import colors
from .theme.spacing import SPACE_1, SPACE_2, SPACE_3, SPACE_5
from .theme.shadows import SHADOW_XL


class SidebarItem(ft.TextButton):
    """Single navigation item used inside :class:`Sidebar`.

    Parameters
    ----------
    data: dict
        Mapping with keys ``id``, ``label``, ``icon`` and optional ``badge``.
    collapsed: bool
        Whether the parent sidebar is currently collapsed.
    selected: bool
        Whether this item represents the current active route.
    on_select: Callable[[str], None]
        Callback fired when the item is activated.
    duration: int
        Animation duration in milliseconds.
    curve: str
        Animation curve name.
    """

    def __init__(
        self,
        data: dict,
        *,
        collapsed: bool,
        selected: bool,
        on_select: Callable[[str], None],
        duration: int,
        curve: str,
    ) -> None:
        super().__init__()
        self._data = data
        self._external_click = data.get("on_click")
        self._on_select = on_select
        self._duration = duration
        self._curve = curve

        self.icon = ft.Icon(data["icon"], size=24)
        self.label = ft.Text(data["label"])
        self.label_container = ft.Container(
            content=self.label,
            opacity=1,
            animate=ft.animation.Animation(duration, curve),
            expand=True,
        )

        controls = [self.icon, self.label_container]
        self.badge: Optional[ft.Control] = None
        badge_val = data.get("badge")
        if badge_val is not None:
            self.badge = ft.Container(
                content=ft.Text(str(badge_val)),
                padding=ft.padding.symmetric(horizontal=SPACE_2, vertical=SPACE_1),
                border_radius=8,
                bgcolor=colors.INDIGO_BG,
                alignment=ft.alignment.center,
                visible=not collapsed,
            )
            controls.append(self.badge)

        self.content = ft.Row(
            controls,
            spacing=SPACE_3,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.height = 48
        self.style = ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=SPACE_3),
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.with_opacity(0.08, colors.TEXT_PRIMARY)
            },
        )
        self.aria_label = data["label"]
        self.on_click = self._handle_click

        self.set_collapsed(collapsed)
        self.set_selected(selected)

    def _handle_click(self, e: ft.ControlEvent) -> None:
        if self._external_click:
            self._external_click(e)
        self._on_select(self._data["id"])

    def set_collapsed(self, collapsed: bool) -> None:
        """Update layout when sidebar collapses or expands."""
        self.label_container.width = 0 if collapsed else None
        self.label_container.opacity = 0 if collapsed else 1
        self.content.alignment = (
            ft.MainAxisAlignment.CENTER if collapsed else ft.MainAxisAlignment.START
        )
        self.tooltip = self.label.value if collapsed else None
        if self.badge:
            self.badge.visible = not collapsed

    def set_selected(self, selected: bool) -> None:
        """Apply visual state for the active item."""
        self.style = ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=SPACE_3),
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor={
                ft.MaterialState.DEFAULT: ft.colors.SECONDARY_CONTAINER
                if selected
                else None,
                ft.MaterialState.HOVERED: ft.colors.with_opacity(
                    0.08, colors.TEXT_PRIMARY
                ),
            },
        )


class Sidebar(ft.Container):
    """Expandable/collapsible navigation sidebar."""

    def __init__(
        self,
        page: ft.Page,
        items: List[dict],
        *,
        collapsed: Optional[bool] = None,
        on_toggle: Optional[Callable[[bool], None]] = None,
        open_width: int = 240,
        closed_width: int = 64,
        duration: int = 180,
        curve: str = "ease",
    ) -> None:
        self.page = page
        self.on_toggle = on_toggle
        self.open_width = max(open_width, 240)
        self.closed_width = min(closed_width, 64)
        self.duration = duration
        self.curve = curve

        stored = self.page.client_storage.get("sidebar_collapsed")
        if collapsed is None:
            collapsed = json.loads(stored) if stored is not None else False
        self.collapsed = collapsed

        self._items: List[SidebarItem] = []
        for data in items:
            item = SidebarItem(
                data,
                collapsed=self.collapsed,
                selected=data.get("selected", False),
                on_select=self._on_item_selected,
                duration=duration,
                curve=curve,
            )
            self._items.append(item)

        self.toggle_btn = ft.IconButton(
            icon=ft.icons.MENU,
            icon_size=24,
            tooltip="Colapsar menu" if not self.collapsed else "Expandir menu",
            aria_label="Colapsar menu" if not self.collapsed else "Expandir menu",
            on_click=self.toggle_sidebar,
            rotate=ft.transform.Rotate(0 if not self.collapsed else math.pi),
            animate_rotation=ft.animation.Animation(duration, curve),
        )

        content = ft.Column(
            [ft.Row([self.toggle_btn], alignment=ft.MainAxisAlignment.END), *self._items],
            spacing=SPACE_3,
            expand=True,
        )

        super().__init__(
            content=content,
            width=self.open_width if not self.collapsed else self.closed_width,
            bgcolor=colors.WHITE,
            padding=ft.padding.all(SPACE_5),
            shadow=SHADOW_XL,
            animate=ft.animation.Animation(duration, curve),
        )

    def _on_item_selected(self, item_id: str) -> None:
        for item in self._items:
            item.set_selected(item._data["id"] == item_id)
        self.update()

    def toggle_sidebar(self, e: Optional[ft.ControlEvent] = None) -> None:
        self.set_collapsed(not self.collapsed)

    def set_collapsed(self, value: bool) -> None:
        self.collapsed = value
        self.width = self.open_width if not value else self.closed_width
        self.toggle_btn.rotate.angle = 0 if not value else math.pi
        label = "Colapsar menu" if not value else "Expandir menu"
        self.toggle_btn.tooltip = label
        self.toggle_btn.aria_label = label
        for item in self._items:
            item.set_collapsed(value)
        self.page.client_storage.set("sidebar_collapsed", json.dumps(value))
        if self.on_toggle:
            self.on_toggle(value)
        self.update()

    def update_layout(self, width: int) -> None:
        if width < 768 and not self.collapsed:
            self.set_collapsed(True)
