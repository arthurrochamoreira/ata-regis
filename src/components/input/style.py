"""Shared styles for input fields."""

from theme.tokens import TOKENS as T
import flet as ft

C, S, R, SH, M, TY = (
    T.colors,
    T.spacing,
    T.radius,
    T.shadows,
    T.motion,
    T.typography,
)


def field_style(*, error: bool = False) -> dict:
    """Return base keyword arguments for text-based inputs."""
    border = C.ERROR_TEXT if error else C.BORDER
    return {
        "bgcolor": C.SURFACE,
        "border_color": border,
        "border_width": 1,
        "border_radius": R.RADIUS_MD,
        "focused_border_color": C.FOCUS_RING_STRONG,
        "focused_border_width": 2,
        "content_padding": ft.padding.symmetric(
            horizontal=S.SPACE_3, vertical=S.SPACE_2
        ),
    }


# Example usage:
# from components.input import style
# base = style.field_style()
