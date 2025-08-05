import flet as ft

SHADOW_XL = ft.BoxShadow(
    blur_radius=25,
    offset=ft.Offset(0, 20),
    color=ft.colors.BLACK12,
)

SHADOW_LG = ft.BoxShadow(
    blur_radius=15,
    offset=ft.Offset(0, 10),
    color=ft.colors.BLACK12,
)

SHADOW_MD = ft.BoxShadow(
    blur_radius=6,
    offset=ft.Offset(0, 4),
    color=ft.colors.BLACK12,
)

__all__ = [
    "SHADOW_XL",
    "SHADOW_LG",
    "SHADOW_MD",
]
