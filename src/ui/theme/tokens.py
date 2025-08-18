"""Unified access point for design tokens.

Import ``TOKENS`` to use shared design values throughout the app.
"""

from types import SimpleNamespace

from . import colors, spacing, typography, sizes, radius, shadows, motion

TOKENS = SimpleNamespace(
    color=colors.SEM,
    colors=colors,
    spacing=spacing,
    typography=typography,
    sizes=sizes,
    radius=radius,
    shadows=shadows,
    motion=motion,
)

# ---------------------------------------------------------------------------
# Future themes can extend/override TOKENS here (e.g., alto contraste)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Migration guide
# ---------------------------------------------------------------------------
# Para localizar números mágicos no código use:
# Pixels: (?<![A-Za-z_])(?:[1-9]\d*|0)(?:\.\d+)?(?=px|\b)
# Cores hex: #(?:[0-9a-fA-F]{3}){1,2}\b
# Substitua por tokens (SPACE_*, ICON_*, RADIUS_*, color.* etc.).
#
# Exemplo de consumo em uma tela:
#     from ui.theme.tokens import TOKENS
#     page.theme = ft.Theme(font_family=TOKENS.typography.FONT_FAMILY)
#     page.bgcolor = TOKENS.color.background
#     ft.Text("Olá", color=TOKENS.color.primary)
# ---------------------------------------------------------------------------

__all__ = ["TOKENS"]
