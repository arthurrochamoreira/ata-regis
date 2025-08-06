from .theme.spacing import (
    SPACE_1,
    SPACE_2,
    SPACE_3,
    SPACE_4,
    SPACE_5,
    SPACE_6,
)
from .theme.shadows import SHADOW_MD
from .theme.typography import (
    text,
    FONT_BOLD,
    LEADING_5,
    TRACKING_WIDER,
    TEXT_XL,
)
from .theme import colors

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
        color=colors.PRIMARY_TEXT,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=9999),
            bgcolor={
                ft.MaterialState.DEFAULT: colors.PRIMARY_BG,
                ft.MaterialState.HOVERED: colors.PRIMARY_HOVER,
            },
        ),
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
            shape=ft.RoundedRectangleBorder(radius=9999),
            color=colors.SECONDARY_TEXT,
            side=ft.BorderSide(1, colors.SECONDARY_BORDER),
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
                border_radius=8,
            ),
            text(
                title,
                size=TEXT_XL,
                weight=FONT_BOLD,
                line_height=LEADING_5,
                letter_spacing=TRACKING_WIDER,
                color=colors.TEXT_PRIMARY,
            ),
        ],
        spacing=SPACE_3,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Column([header, body], spacing=SPACE_5),
        bgcolor=colors.CARD_BG,
        padding=SPACE_4,
        border_radius=8,
    )

def build_card(title: str, icon: ft.Control, content: ft.Control) -> ft.Control:
    header = ft.Row(
        [
            icon,
            text(
                title,
                size=16,
                weight=ft.FontWeight.W_600,
                line_height=LEADING_5,
                letter_spacing=TRACKING_WIDER,
                color=colors.TEXT_PRIMARY,
            ),
        ],
        spacing=SPACE_2,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return ft.Container(
        content=ft.Column([header, content], spacing=SPACE_4),
        padding=SPACE_4,
        border=ft.border.all(1, colors.GREY_LIGHT),
        border_radius=8,
        bgcolor=colors.WHITE,
        shadow=SHADOW_MD,
    )
