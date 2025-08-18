from .theme.spacing import (
    SPACE_2,
    SPACE_3,
    SPACE_4,
    SPACE_5,
)
from .theme.shadows import SHADOW_MD
from .theme.typography import (
    text,
    H2,
    H3,
    BUTTON,
)
from .theme import colors

import flet as ft
from typing import Callable, Optional


def primary_button(
    label: str,
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

    label_control = text(label, **BUTTON, color=colors.SEM.surface)

    if icon:
        content = ft.Row(
            [ft.Icon(icon, color=colors.SEM.surface), label_control],
            spacing=SPACE_2,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        content = label_control

    return ft.ElevatedButton(
        content=content,
        on_click=on_click,
        bgcolor=colors.SEM.primary,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=9999),
        ),
        **kwargs,
    )


def secondary_button(
    label: str,
    *,
    icon: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
    **kwargs,
) -> ft.OutlinedButton:
    """Return a standard secondary button used across the app.

    ``kwargs`` are passed to the underlying button allowing controls to specify
    responsive parameters like ``expand`` or ``col``.
    """

    label_control = text(label, **BUTTON, color=colors.SEM.text)

    if icon:
        content = ft.Row(
            [ft.Icon(icon, color=colors.SEM.text), label_control],
            spacing=SPACE_2,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        content = label_control

    return ft.OutlinedButton(
        content=content,
        on_click=on_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=9999),
            side=ft.BorderSide(1, colors.SEM.border),
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
                **H2,
                color=colors.SEM.text,
            ),
        ],
        spacing=SPACE_3,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Column([header, body], spacing=SPACE_5),
        bgcolor=colors.SEM.surface,
        padding=SPACE_4,
        border_radius=8,
    )

def build_card(title: str, icon: ft.Control, content: ft.Control) -> ft.Control:
    header = ft.Row(
        [
            icon,
            text(
                title,
                **H3,
                color=colors.SEM.text,
            ),
        ],
        spacing=SPACE_2,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return ft.Container(
        content=ft.Column([header, content], spacing=SPACE_4),
        padding=SPACE_4,
        border=ft.border.all(1, colors.SEM.border),
        border_radius=8,
        bgcolor=colors.SEM.surface,
        shadow=SHADOW_MD,
    )
