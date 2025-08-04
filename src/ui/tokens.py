from .spacing import (
    SPACE_1,
    SPACE_2,
    SPACE_3,
    SPACE_4,
    SPACE_5,
    SPACE_6,
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
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
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
            shape=ft.RoundedRectangleBorder(radius=8),
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
            ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
        ],
        spacing=SPACE_3,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Column([header, body], spacing=SPACE_5),
        bgcolor=CARD_BG,
        padding=SPACE_4,
        border_radius=12,
    )

def build_card(title: str, icon: ft.Control, content: ft.Control) -> ft.Control:
    header = ft.Row(
        [
            icon,
            ft.Text(
                title,
                size=16,
                weight=ft.FontWeight.W_600,
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
        border_radius=12,
        bgcolor=ft.colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=6,
            color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
    )
