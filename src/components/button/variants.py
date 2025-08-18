"""Button variant components.

Provides styled button controls consistent with the design tokens.
"""

from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from theme.tokens import TOKENS as T
from . import sizing

C, S, R, SH, M, TY = (
    T.colors,
    T.spacing,
    T.radius,
    T.shadows,
    T.motion,
    T.typography,
)


def _content(
    text: str,
    size: str,
    *,
    text_color: str,
    icon: Optional[str] = None,
    trailing_icon: Optional[str] = None,
    loading: bool = False,
) -> ft.Row:
    items: list[ft.Control] = []
    if loading:
        items.append(
            ft.ProgressRing(
                width=sizing.ICON_SIZE[size],
                height=sizing.ICON_SIZE[size],
                color=text_color,
            )
        )
    if icon:
        items.append(ft.Icon(icon, size=sizing.ICON_SIZE[size], color=text_color))
    items.append(
        ft.Text(
            text,
            size=sizing.TEXT_SIZE[size],
            color=text_color,
            weight=ft.FontWeight.W_500,
        )
    )
    if trailing_icon:
        items.append(
            ft.Icon(trailing_icon, size=sizing.ICON_SIZE[size], color=text_color)
        )
    return ft.Row(items, spacing=S.SPACE_2, alignment=ft.MainAxisAlignment.CENTER)


def _primary_style(size: str) -> ft.ButtonStyle:
    return ft.ButtonStyle(
        bgcolor={
            "": C.PRIMARY,
            "hovered": C.PRIMARY_HOVER,
            "pressed": C.PRIMARY_ACTIVE,
            "disabled": C.BORDER,
        },
        padding=sizing.PADDING[size],
        shape=ft.RoundedRectangleBorder(radius=R.RADIUS_MD),
        side={"focused": ft.BorderSide(2, C.FOCUS_RING_STRONG)},
    )


def _secondary_style(size: str) -> ft.ButtonStyle:
    return ft.ButtonStyle(
        bgcolor={"": C.SURFACE, "hovered": C.NEUTRAL_50},
        color={"": C.NEUTRAL_700, "disabled": C.TEXT_MUTED},
        padding=sizing.PADDING[size],
        side={
            "": ft.BorderSide(1, C.BORDER),
            "focused": ft.BorderSide(2, C.FOCUS_RING_STRONG),
        },
        shape=ft.RoundedRectangleBorder(radius=R.RADIUS_MD),
    )


def _icon_action_style() -> ft.ButtonStyle:
    return ft.ButtonStyle(
        color={"": C.TEXT_MUTED, "hovered": C.PRIMARY},
        side={"focused": ft.BorderSide(2, C.FOCUS_RING_STRONG)},
        shape=ft.CircleBorder(),
        padding=ft.padding.all(0),
    )


def PrimaryButton(
    text: str,
    *,
    size: str = "md",
    icon: Optional[str] = None,
    trailing_icon: Optional[str] = None,
    full_width: bool = False,
    loading: bool = False,
    disabled: bool = False,
    tooltip: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
) -> ft.Container:
    """Filled primary action button."""

    btn = ft.ElevatedButton(
        content=_content(
            text,
            size,
            text_color=C.SURFACE,
            icon=icon,
            trailing_icon=trailing_icon,
            loading=loading,
        ),
        style=_primary_style(size),
        tooltip=tooltip,
        on_click=on_click,
        disabled=disabled or loading,
        expand=1 if full_width else 0,
    )
    return ft.Container(content=btn, shadow=SH.SHADOW_SM)


def SecondaryButton(
    text: str,
    *,
    size: str = "md",
    icon: Optional[str] = None,
    trailing_icon: Optional[str] = None,
    full_width: bool = False,
    loading: bool = False,
    disabled: bool = False,
    tooltip: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
) -> ft.Container:
    """Outlined secondary action button."""

    text_color = C.NEUTRAL_700 if not (disabled or loading) else C.TEXT_MUTED
    btn = ft.OutlinedButton(
        content=_content(
            text,
            size,
            text_color=text_color,
            icon=icon,
            trailing_icon=trailing_icon,
            loading=loading,
        ),
        style=_secondary_style(size),
        tooltip=tooltip,
        on_click=on_click,
        disabled=disabled or loading,
        expand=1 if full_width else 0,
    )
    return ft.Container(content=btn)


def IconAction(
    icon: str,
    *,
    tooltip: Optional[str] = None,
    size: str = "md",
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
    disabled: bool = False,
) -> ft.IconButton:
    """Icon-only action button with hover feedback."""

    return ft.IconButton(
        icon=icon,
        tooltip=tooltip,
        on_click=on_click,
        disabled=disabled,
        icon_size=sizing.ICON_SIZE[size],
        style=_icon_action_style(),
    )


# Example usage:
# btn = PrimaryButton("Nova Ata")
# sec = SecondaryButton("Limpar")
# act = IconAction(ft.icons.EDIT)
