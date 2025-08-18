"""Button sizing tokens."""

from theme.tokens import TOKENS as T
import flet as ft

S, TY = T.spacing, T.typography

PADDING = {
    "sm": ft.padding.symmetric(horizontal=S.SPACE_3, vertical=S.SPACE_2),
    "md": ft.padding.symmetric(horizontal=S.SPACE_4, vertical=S.SPACE_2),
    "lg": ft.padding.symmetric(horizontal=S.SPACE_5, vertical=S.SPACE_3),
}

ICON_SIZE = {
    "sm": T.sizes.ICON_SM,
    "md": T.sizes.ICON_MD,
    "lg": T.sizes.ICON_LG,
}

TEXT_SIZE = {
    "sm": TY.TEXT_SM,
    "md": TY.TEXT_BASE,
    "lg": TY.TEXT_LG,
}

# Example usage:
# from components.button import sizing
# btn_padding = sizing.PADDING["md"]
