"""Shared styles for input fields."""

from theme.tokens import TOKENS as T

C, R = T.colors, T.radius


def field_style() -> dict:
    """Return default style keyword arguments for inputs."""
    return {
        "border_color": C.SECONDARY_BORDER,
        "focused_border_color": C.FOCUSED_BORDER,
        "focused_border_width": 2,
        "border_radius": R.RADIUS_SM,
    }
