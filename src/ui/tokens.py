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

import flet as ft
from typing import Callable, Optional

PRIMARY = ft.colors.BLUE
DANGER = ft.colors.RED
SUCCESS = ft.colors.GREEN
WARNING = ft.colors.ORANGE
GREY_LIGHT = ft.colors.GREY_300
CARD_BG = "#F8FAFC"


def primary_button(
    text: str,
    *,
    icon: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
) -> ft.ElevatedButton:
    """Return a standard primary button used across the app."""

    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        bgcolor="#3B82F6",
        color="#FFFFFF",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=9999)),
    )


def secondary_button(
    text: str,
    *,
    icon: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
) -> ft.OutlinedButton:
    """Return a standard secondary button used across the app."""

    return ft.OutlinedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=9999),
            color="#4B5563",
            side=ft.BorderSide(1, "#D1D5DB"),
        ),
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
                color="#1F2937",
            ),
        ],
        spacing=SPACE_3,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Column([header, body], spacing=SPACE_5),
        bgcolor=CARD_BG,
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
                color="#1F2937",
            ),
        ],
        spacing=SPACE_2,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return ft.Container(
        content=ft.Column([header, content], spacing=SPACE_4),
        padding=SPACE_4,
        border=ft.border.all(1, GREY_LIGHT),
        border_radius=8,
        bgcolor=ft.colors.WHITE,
        shadow=SHADOW_MD,
    )
