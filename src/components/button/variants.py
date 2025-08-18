"""Public button variants."""

from typing import Callable, Optional
import flet as ft

from theme.tokens import TOKENS as T
from . import style, sizing

C = T.colors


def PrimaryButton(
    text: str,
    *,
    icon: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
    size: str = "md",
    **kwargs,
) -> ft.ElevatedButton:
    """Filled primary action button."""
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        style=style.primary(size),
        **kwargs,
    )


def SecondaryButton(
    text: str,
    *,
    icon: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
    size: str = "md",
    **kwargs,
) -> ft.OutlinedButton:
    """Outlined secondary action button."""
    return ft.OutlinedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        style=style.secondary(size),
        **kwargs,
    )


def IconAction(
    icon: str,
    *,
    tooltip: Optional[str] = None,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
    hover_color: str,
    size: str = "md",
    **kwargs,
) -> ft.IconButton:
    """Icon-only action button with hover feedback."""
    return ft.IconButton(
        icon=icon,
        tooltip=tooltip,
        on_click=on_click,
        style=style.icon_action(hover_color),
        icon_size=sizing.ICON_SIZE[size],
        **kwargs,
    )
