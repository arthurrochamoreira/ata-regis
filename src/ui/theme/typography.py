import flet as ft
from typing import Any

# Default font family with fallbacks
FONT_FAMILY = "Inter, system-ui, Arial"
# Backwards compatibility
FONT_SANS = FONT_FAMILY

# ---------------------------------------------------------------------------
# Typography scale
# ---------------------------------------------------------------------------
H2 = {"size": 30, "weight": "w700", "line_height": 36}
H3 = {"size": 14, "weight": "w600", "line_height": 20}
BODY = {"size": 14, "weight": "w400", "line_height": 20}
LABEL = {"size": 12, "weight": "w500", "line_height": 16}
BUTTON = {"size": 14, "weight": "w600", "line_height": 20}

# Legacy size tokens preserved for compatibility
TEXT_XL = 20  # text-xl
TEXT_LG = 18  # text-lg
TEXT_BASE = 16  # base text
TEXT_SM = 14  # text-sm
TEXT_XS = 11  # text-xs

# Font weight tokens
FONT_BOLD = ft.FontWeight.BOLD

# Line height and letter spacing tokens
LEADING_5 = 1.25
TRACKING_WIDER = 0.05


def text(
    value: str,
    *,
    size: int | float = TEXT_SM,
    weight: str | ft.FontWeight | None = None,
    line_height: int | float | None = None,
    letter_spacing: float | None = None,
    color: str | None = None,
    **kwargs: Any,
) -> ft.Text:
    """Create a Text control with the project default font settings."""
    return ft.Text(
        value,
        style=ft.TextStyle(
            font_family=FONT_FAMILY,
            size=size,
            weight=weight,
            height=line_height,
            letter_spacing=letter_spacing,
            color=color,
        ),
        **kwargs,
    )


def text_style(
    *,
    size: int | float = TEXT_SM,
    weight: str | ft.FontWeight | None = None,
    line_height: int | float | None = None,
    letter_spacing: float | None = None,
    color: str | None = None,
) -> ft.TextStyle:
    """Return a TextStyle with default font family and given parameters."""
    return ft.TextStyle(
        font_family=FONT_FAMILY,
        size=size,
        weight=weight,
        height=line_height,
        letter_spacing=letter_spacing,
        color=color,
    )

__all__ = [
    "FONT_FAMILY",
    "FONT_SANS",
    "H2",
    "H3",
    "BODY",
    "LABEL",
    "BUTTON",
    "TEXT_XL",
    "TEXT_LG",
    "TEXT_BASE",
    "TEXT_SM",
    "TEXT_XS",
    "FONT_BOLD",
    "LEADING_5",
    "TRACKING_WIDER",
    "text",
    "text_style",
]
