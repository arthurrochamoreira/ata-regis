"""Legacy helpers and section builders."""

from theme.tokens import TOKENS as T
from theme.typography import text
from components import PrimaryButton, SecondaryButton
import flet as ft
import warnings

C, S, SH, TY = T.colors, T.spacing, T.shadows, T.typography


def primary_button(*args, **kwargs):
    """Deprecated: use :func:`components.PrimaryButton`."""
    warnings.warn("primary_button is deprecated; use components.PrimaryButton", DeprecationWarning, stacklevel=2)
    return PrimaryButton(*args, **kwargs)


def secondary_button(*args, **kwargs):
    """Deprecated: use :func:`components.SecondaryButton`."""
    warnings.warn("secondary_button is deprecated; use components.SecondaryButton", DeprecationWarning, stacklevel=2)
    return SecondaryButton(*args, **kwargs)


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
    """Return a card with icon and content."""
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

__all__ = [
    "primary_button",
    "secondary_button",
    "build_section",
    "build_card",
]
