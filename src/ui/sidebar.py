import json
import math
from typing import Callable, List, Optional

import flet as ft

from .theme import colors
from .theme.spacing import SPACE_1, SPACE_2, SPACE_3, SPACE_5
from .theme.sizes import (
    WIDTH_SIDEBAR_OPEN,
    WIDTH_SIDEBAR_COLLAPSED,
    ITEM_TOUCH,
    ICON_MD,
)
from .theme.shadows import SHADOW_XL


class SidebarItem(ft.Container):
    """Single navigation item used inside :class:`Sidebar`."""

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
        super().__init__(padding=0)
        self._data = data
        self._external_click = data.get("on_click")
        self._on_select = on_select

        icon_expanded = ft.Icon(data["icon"], size=ICON_MD)
        label = ft.Text(data["label"])
        row_controls: List[ft.Control] = [icon_expanded, label]
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
            row_controls.append(self.badge)

        self._row_btn = ft.TextButton(
            content=ft.Row(
                row_controls,
                spacing=SPACE_3,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=WIDTH_SIDEBAR_OPEN,
            height=ITEM_TOUCH,
            on_click=self._handle_click,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=SPACE_3),
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor={
                    ft.MaterialState.HOVERED: ft.colors.with_opacity(
                        0.08, colors.TEXT_PRIMARY
                    )
                },
            ),
        )
        self._row_btn.aria_label = data["label"]

        self._icon_btn = ft.IconButton(
            icon=data["icon"],
            icon_size=ICON_MD,
            width=WIDTH_SIDEBAR_COLLAPSED,
            height=ITEM_TOUCH,
            tooltip=data["label"] if collapsed else None,
            on_click=self._handle_click,
            style=ft.ButtonStyle(
                padding=0,
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor={
                    ft.MaterialState.HOVERED: ft.colors.with_opacity(
                        0.08, colors.TEXT_PRIMARY
                    )
                },
            ),
        )
        self._icon_btn.aria_label = data["label"]

        self.width = WIDTH_SIDEBAR_COLLAPSED if collapsed else WIDTH_SIDEBAR_OPEN
        self.height = ITEM_TOUCH
        self.alignment = ft.alignment.center
        self.content = self._icon_btn if collapsed else self._row_btn

        self.set_selected(selected)

    def _handle_click(self, e: ft.ControlEvent) -> None:
        if self._external_click:
            self._external_click(e)
        self._on_select(self._data["id"])

    def set_collapsed(self, collapsed: bool) -> None:
        """Update layout when sidebar collapses or expands."""
        self.content = self._icon_btn if collapsed else self._row_btn
        self.width = WIDTH_SIDEBAR_COLLAPSED if collapsed else WIDTH_SIDEBAR_OPEN
        self._icon_btn.tooltip = self._data["label"] if collapsed else None
        if self.badge:
            self.badge.visible = not collapsed
        self.update()

    def set_selected(self, selected: bool) -> None:
        """Apply visual state for the active item."""
        bg = ft.colors.SECONDARY_CONTAINER if selected else None
        self._row_btn.style = ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=SPACE_3),
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor={
                ft.MaterialState.DEFAULT: bg,
                ft.MaterialState.HOVERED: ft.colors.with_opacity(
                    0.08, colors.TEXT_PRIMARY
                ),
            },
        )
        self._icon_btn.style = ft.ButtonStyle(
            padding=0,
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor={
                ft.MaterialState.DEFAULT: bg,
                ft.MaterialState.HOVERED: ft.colors.with_opacity(
                    0.08, colors.TEXT_PRIMARY
                ),
            },
        )
        self.update()


class Sidebar(ft.Container):
    """Expandable/collapsible navigation sidebar."""

    def __init__(
        self,
        page: ft.Page,
        items: List[dict],
        *,
        collapsed: Optional[bool] = None,
        on_toggle: Optional[Callable[[bool], None]] = None,
        open_width: int = WIDTH_SIDEBAR_OPEN,
        closed_width: int = WIDTH_SIDEBAR_COLLAPSED,
        duration: int = 180,
        curve: str = "ease",
    ) -> None:
        self.page = page
        self.on_toggle = on_toggle
        self.open_width = max(open_width, WIDTH_SIDEBAR_OPEN)
        self.closed_width = min(closed_width, WIDTH_SIDEBAR_COLLAPSED)
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
            icon_size=ICON_MD,
            tooltip="Colapsar menu" if not self.collapsed else "Expandir menu",
            on_click=self.toggle_sidebar,
            rotate=ft.transform.Rotate(0 if not self.collapsed else math.pi),
            animate_rotation=ft.animation.Animation(duration, curve),
            padding=0,
        )
        self.toggle_btn.aria_label = (
            "Colapsar menu" if not self.collapsed else "Expandir menu"
        )

        content = ft.Column(
            [ft.Row([self.toggle_btn], alignment=ft.MainAxisAlignment.END), *self._items],
            spacing=SPACE_2,
            expand=True,
        )

        super().__init__(
            content=content,
            width=self.open_width if not self.collapsed else self.closed_width,
            bgcolor=colors.WHITE,
            padding=ft.padding.symmetric(vertical=SPACE_5),
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
