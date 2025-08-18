"""Shared styles for input fields."""

from theme.tokens import TOKENS as T
from theme import colors as C

R = T.radius


def field_style() -> dict:
    """Return default style keyword arguments for inputs."""
    return {
        "border_color": C.BORDER,
        "focused_border_color": C.PRIMARY,
        "focused_border_width": 2,
        "border_radius": R.RADIUS_SM,
    }
