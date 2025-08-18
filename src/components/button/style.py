"""Button style definitions."""

import flet as ft
from theme.tokens import TOKENS as T
from theme import colors as C
from . import sizing

R = T.radius


def primary(size: str = "md") -> ft.ButtonStyle:
    """Return style for primary buttons."""
    return ft.ButtonStyle(
        color={"": "#FFFFFF", "disabled": C.TEXT_SECONDARY},
        bgcolor={
            "": C.PRIMARY,
            "hovered": C.PRIMARY_HOVER,
            "pressed": C.PRIMARY_ACTIVE,
            "disabled": C.BORDER,
        },
        padding=sizing.PADDING[size],
        shape=ft.RoundedRectangleBorder(radius=R.RADIUS_FULL),
    )


def secondary(size: str = "md") -> ft.ButtonStyle:
    """Return style for secondary buttons."""
    return ft.ButtonStyle(
        color={"": C.TEXT_PRIMARY, "disabled": C.TEXT_SECONDARY},
        bgcolor={"hovered": C.BG_APP},
        padding=sizing.PADDING[size],
        side=ft.BorderSide(1, C.BORDER),
        shape=ft.RoundedRectangleBorder(radius=R.RADIUS_FULL),
    )


def icon_action(hover_color: str) -> ft.ButtonStyle:
    """Return style for action icon buttons."""
    return ft.ButtonStyle(
        color={"": C.TEXT_SECONDARY, "hovered": hover_color},
    )
