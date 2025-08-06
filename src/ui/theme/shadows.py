import flet as ft
from . import colors

SHADOW_XL = ft.BoxShadow(
    blur_radius=25,
    offset=ft.Offset(0, 20),
    color=colors.SHADOW_COLOR,
)

SHADOW_LG = ft.BoxShadow(
    blur_radius=15,
    offset=ft.Offset(0, 10),
    color=colors.SHADOW_COLOR,
)

SHADOW_MD = ft.BoxShadow(
    blur_radius=6,
    offset=ft.Offset(0, 4),
    color=colors.SHADOW_COLOR,
)

__all__ = [
    "SHADOW_XL",
    "SHADOW_LG",
    "SHADOW_MD",
]
