"""Button sizing tokens."""

from theme.tokens import TOKENS as T
import flet as ft

S = T.spacing
Z = T.sizes

PADDING = {
    "sm": ft.padding.symmetric(horizontal=S.SPACE_3, vertical=S.SPACE_2),
    "md": ft.padding.symmetric(horizontal=S.SPACE_4, vertical=S.SPACE_2),
    "lg": ft.padding.symmetric(horizontal=S.SPACE_5, vertical=S.SPACE_3),
}

ICON_SIZE = {
    "sm": Z.ICON_SM,
    "md": Z.ICON_MD,
    "lg": Z.ICON_LG,
}
