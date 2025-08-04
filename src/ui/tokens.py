SPACE_1 = 4
SPACE_2 = 8
SPACE_3 = 12
SPACE_4 = 16
SPACE_5 = 24
SPACE_6 = 32

import flet as ft
from typing import Callable, Optional

PRIMARY = ft.colors.BLUE
DANGER = ft.colors.RED
SUCCESS = ft.colors.GREEN
WARNING = ft.colors.ORANGE
GREY_LIGHT = ft.colors.GREY_300
CARD_BG = "#F8FAFC"

BUTTON_HEIGHT = 40


def button_style(**kwargs) -> ft.ButtonStyle:
    return ft.ButtonStyle(
        padding=ft.padding.symmetric(horizontal=16, vertical=0),
        shape=ft.RoundedRectangleBorder(radius=6),
        **kwargs,
    )


def primary_button(
    text: str,
    *,
    icon: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        bgcolor="#3B82F6",
        color="#FFFFFF",
        height=BUTTON_HEIGHT,
        min_width=120,
        style=button_style(),
    )


def secondary_button(
    text: str,
    *,
    icon: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        height=BUTTON_HEIGHT,
        style=button_style(color="#4B5563", side=ft.BorderSide(1, "#D1D5DB")),
    )


def text_button(
    text: str,
    *,
    icon: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
) -> ft.TextButton:
    return ft.TextButton(
        text=text,
        icon=icon,
        on_click=on_click,
        height=BUTTON_HEIGHT,
        style=button_style(),
    )


def icon_button(
    icon: str,
    *,
    tooltip: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
    icon_size: int = 20,
    style: ft.ButtonStyle | None = None,
) -> ft.IconButton:
    return ft.IconButton(
        icon=icon,
        tooltip=tooltip,
        on_click=on_click,
        icon_size=icon_size,
        height=BUTTON_HEIGHT,
        style=style or button_style(),
    )


def build_section(
    title: str,
    icon_name: str,
    icon_color: str,
    icon_bg: str,
    body: ft.Control,
) -> ft.Container:
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

