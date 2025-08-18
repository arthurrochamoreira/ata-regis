"""Button style definitions."""

import flet as ft
from theme.tokens import TOKENS as T
from . import sizing

C, R = T.colors, T.radius


def primary(size: str = "md") -> ft.ButtonStyle:
    """Return style for primary buttons."""
    return ft.ButtonStyle(
        color={"": C.PRIMARY_TEXT, "disabled": C.TEXT_MUTED},
        bgcolor={"": C.PRIMARY_BG, "hovered": C.BLUE_HOVER, "disabled": C.GREY_LIGHT},
        padding=sizing.PADDING[size],
        shape=ft.RoundedRectangleBorder(radius=R.RADIUS_FULL),
    )


def secondary(size: str = "md") -> ft.ButtonStyle:
    """Return style for secondary buttons."""
    return ft.ButtonStyle(
        color={"": C.SECONDARY_TEXT, "disabled": C.TEXT_MUTED},
        bgcolor={"hovered": C.GREY_LIGHT},
        padding=sizing.PADDING[size],
        side=ft.BorderSide(1, C.SECONDARY_BORDER),
        shape=ft.RoundedRectangleBorder(radius=R.RADIUS_FULL),
    )


def icon_action(hover_color: str) -> ft.ButtonStyle:
    """Return style for action icon buttons."""
    return ft.ButtonStyle(
        color={"": C.TEXT_SECONDARY, "hovered": hover_color},
    )
