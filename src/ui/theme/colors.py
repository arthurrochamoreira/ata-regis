import flet as ft
from types import SimpleNamespace

# ---------------------------------------------------------------------------
# Base palette
# ---------------------------------------------------------------------------
# Alterar valores aqui caso a paleta base do projeto mude no futuro.
WHITE = ft.colors.WHITE
BLACK = ft.colors.BLACK
TRANSPARENT = ft.colors.TRANSPARENT
INVERSE_PRIMARY = ft.colors.INVERSE_PRIMARY
SURFACE_VARIANT = ft.colors.SURFACE_VARIANT
PAGE_BG = "#F3F4F6"
CARD_BG = "#F8FAFC"

# Text colors
TEXT_DARK = "#111827"
TEXT_PRIMARY = "#1F2937"
TEXT_SECONDARY = "#6B7280"
TEXT_MUTED = "#374151"
TEXT_ON_DARK = ft.colors.WHITE
TEXT_LABEL = ft.colors.SECONDARY
TEXT_SUCCESS = ft.colors.GREEN
TEXT_WARNING = ft.colors.ORANGE
TEXT_ERROR = ft.colors.RED
TEXT_INFO = ft.colors.BLUE

# Button colors
PRIMARY_BG = "#3B82F6"
PRIMARY_TEXT = "#FFFFFF"
SECONDARY_TEXT = "#4B5563"
SECONDARY_BORDER = "#D1D5DB"
FOCUSED_BORDER = "#3B82F6"

# Neutral colors
GREY_LIGHT = "#E5E7EB"
GREY_DIVIDER = "#9CA3AF"
HEADER_BG = "#F9FAFB"

# Section colors
INDIGO = "#4F46E5"
INDIGO_BG = "#E0E7FF"
ORANGE = "#EA580C"
ORANGE_BG = "#FFEDD5"
TEAL = "#0F766E"
TEAL_BG = "#CCFBF1"

# Status colors
GREEN = "#16A34A"
GREEN_BG = "#D1FAE5"
GREEN_DARK = "#14532D"
YELLOW = "#CA8A04"
YELLOW_BG = "#FEF9C3"
YELLOW_DARK = "#713F12"
RED = "#DC2626"
RED_BG = "#FEE2E2"
RED_DARK = "#991B1B"
BLUE_HOVER = "#2563EB"
RESUMO_BG = "#EEF2FF"
GREEN_50 = ft.colors.GREEN_50
ORANGE_50 = ft.colors.ORANGE_50
RED_50 = ft.colors.RED_50
BLUE_50 = ft.colors.BLUE_50
GREEN_200 = ft.colors.GREEN_200
ORANGE_200 = ft.colors.ORANGE_200
RED_200 = ft.colors.RED_200

# Semantic aliases
PRIMARY = ft.colors.BLUE
DANGER = ft.colors.RED
SUCCESS = ft.colors.GREEN
WARNING = ft.colors.ORANGE
OUTLINE = ft.colors.OUTLINE


# ---------------------------------------------------------------------------
# Semantic color mapping
# ---------------------------------------------------------------------------
# Use ``color.<token>`` instead de valores hexadecimais no código.
# Para alterar o tema, mapeie esses tokens para cores diferentes.
color = SimpleNamespace(
    primary=PRIMARY_BG,
    surface=CARD_BG,
    background=PAGE_BG,
    text=TEXT_PRIMARY,
    muted=TEXT_SECONDARY,
    border=SECONDARY_BORDER,
    error=RED,
    focus_ring=FOCUSED_BORDER,
)

__all__ = [name for name in globals().keys() if name.isupper()] + ["color"]
