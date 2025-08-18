from ui.theme.tokens import TOKENS as T
from ui.theme.typography import text

C, S, SH, TY = T.colors, T.spacing, T.shadows, T.typography

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
        bgcolor=C.PRIMARY_BG,
        color=C.PRIMARY_TEXT,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=9999)),
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
            color=C.SECONDARY_TEXT,
            side=ft.BorderSide(1, C.SECONDARY_BORDER),
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
                padding=S.SPACE_2,
                border_radius=8,
            ),
            text(
                title,
                size=TY.TEXT_XL,
                weight=TY.FONT_BOLD,
                line_height=TY.LEADING_5,
                letter_spacing=TY.TRACKING_WIDER,
                color=C.TEXT_PRIMARY,
            ),
        ],
        spacing=S.SPACE_3,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Column([header, body], spacing=S.SPACE_5),
        bgcolor=C.CARD_BG,
        padding=S.SPACE_4,
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
                line_height=TY.LEADING_5,
                letter_spacing=TY.TRACKING_WIDER,
                color=C.TEXT_PRIMARY,
            ),
        ],
        spacing=S.SPACE_2,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return ft.Container(
        content=ft.Column([header, content], spacing=S.SPACE_4),
        padding=S.SPACE_4,
        border=ft.border.all(1, C.GREY_LIGHT),
        border_radius=8,
        bgcolor=C.WHITE,
        shadow=SH.SHADOW_MD,
    )
