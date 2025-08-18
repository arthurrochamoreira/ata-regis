import flet as ft

# Standard shadows
# Use SHADOW_SM for cards, SHADOW_MD for navegação/surfaces,
# and SHADOW_XL for overlays e diálogos.
SHADOW_SM = ft.BoxShadow(
    blur_radius=6,
    offset=ft.Offset(0, 4),
    color=ft.colors.BLACK12,
)

SHADOW_MD = ft.BoxShadow(
    blur_radius=15,
    offset=ft.Offset(0, 10),
    color=ft.colors.BLACK12,
)

# Backwards compatibility alias
SHADOW_LG = SHADOW_MD

SHADOW_XL = ft.BoxShadow(
    blur_radius=25,
    offset=ft.Offset(0, 20),
    color=ft.colors.BLACK12,
)

__all__ = ["SHADOW_SM", "SHADOW_MD", "SHADOW_XL", "SHADOW_LG"]
