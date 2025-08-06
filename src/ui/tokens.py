from .ui_tokens import (
    SPACE_1,
    SPACE_2,
    SPACE_3,
    SPACE_4,
    SPACE_5,
    SPACE_6,
    PRIMARY,
    SUCCESS,
    WARNING,
    DANGER,
    NEUTRAL,
    BORDER,
    RADIUS_PILL,
)
from .theme.shadows import SHADOW_MD
from .theme.typography import (
    text,
    FONT_BOLD,
    LEADING_5,
    TRACKING_WIDER,
    TEXT_XL,
)

import flet as ft
from typing import Callable, Optional


def primary_button(
    text: str,
    *,
    icon: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
    **kwargs,
) -> ft.ElevatedButton:
    """Return a standard primary button used across the app.

    Additional ``kwargs`` are forwarded to :class:`flet.ElevatedButton` so
    callers can specify properties like ``expand`` or ``col`` to make buttons
    responsive inside ``ResponsiveRow`` containers.
    """

    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        bgcolor=PRIMARY,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=RADIUS_PILL)),
        **kwargs,
    )


def secondary_button(
    text: str,
    *,
    icon: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
    **kwargs,
) -> ft.OutlinedButton:
    """Return a standard secondary button used across the app.

    ``kwargs`` are passed to the underlying button allowing controls to specify
    responsive parameters like ``expand`` or ``col``.
    """

    return ft.OutlinedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=RADIUS_PILL),
            color=PRIMARY,
            side=ft.BorderSide(1, BORDER),
        ),
        **kwargs,
    )

def build_section(
    title: str,
    icon_name: str,
    icon_color: str,
    icon_bg: str,
    body: ft.Control,
) -> ft.Container:
    """Return standard section container used across views."""

    header = ft.Row(
        [
            ft.Container(
                content=ft.Icon(icon_name, color=icon_color),
                bgcolor=icon_bg,
                padding=SPACE_2,
                border_radius=SPACE_2,
            ),
            text(
                title,
                size=TEXT_XL,
                weight=FONT_BOLD,
                line_height=LEADING_5,
                letter_spacing=TRACKING_WIDER,
                color=ft.colors.BLACK,
            ),
        ],
        spacing=SPACE_3,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Column([header, body], spacing=SPACE_5),
        bgcolor=NEUTRAL,
        padding=SPACE_4,
        border_radius=SPACE_2,
    )

def build_card(title: str, icon: ft.Control, content: ft.Control) -> ft.Control:
    header = ft.Row(
        [
            icon,
            text(
                title,
                size=TEXT_XL,
                weight=ft.FontWeight.W_600,
                line_height=LEADING_5,
                letter_spacing=TRACKING_WIDER,
                color=ft.colors.BLACK,
            ),
        ],
        spacing=SPACE_2,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return ft.Container(
        content=ft.Column([header, content], spacing=SPACE_4),
        padding=SPACE_4,
        border=ft.border.all(1, BORDER),
        border_radius=SPACE_2,
        bgcolor=ft.colors.WHITE,
        shadow=SHADOW_MD,
    )
