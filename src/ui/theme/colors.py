import flet as ft
from types import SimpleNamespace

# ---------------------------------------------------------------------------
# Base palette
# ---------------------------------------------------------------------------
# Tailwind bg-blue-600
PRIMARY_600 = "#2563EB"  # Azul primário
# Tailwind bg-gray-100
BACKGROUND = "#F3F4F6"  # Cinza fundo principal
# Tailwind bg-white
SURFACE = "#FFFFFF"  # Superfície
# Tailwind text-gray-800
TEXT = "#1F2937"  # Texto principal
# Tailwind text-gray-500
TEXT_MUTED = "#6B7280"  # Texto secundário
# Tailwind border-gray-300
BORDER = "#D1D5DB"  # Bordas

# ---------------------------------------------------------------------------
# Status colors
# ---------------------------------------------------------------------------
# Tailwind bg-green-100
SUCCESS_BG = "#DCFCE7"  # Sucesso fundo
# Tailwind text-green-800
SUCCESS_TEXT = "#166534"  # Sucesso texto
# Tailwind bg-yellow-100
WARNING_BG = "#FEF9C3"  # Atenção fundo
# Tailwind text-yellow-800
WARNING_TEXT = "#854D0E"  # Atenção texto
# Tailwind bg-red-100
ERROR_BG = "#FEE2E2"  # Erro fundo
# Tailwind text-red-800
ERROR_TEXT = "#991B1B"  # Erro texto

# ---------------------------------------------------------------------------
# Semantic mapping
# ---------------------------------------------------------------------------
SEM = SimpleNamespace(
    primary=PRIMARY_600,
    background=BACKGROUND,
    surface=SURFACE,
    text=TEXT,
    muted=TEXT_MUTED,
    border=BORDER,
    success_bg=SUCCESS_BG,
    success_text=SUCCESS_TEXT,
    warning_bg=WARNING_BG,
    warning_text=WARNING_TEXT,
    error_bg=ERROR_BG,
    error_text=ERROR_TEXT,
    focus_ring=PRIMARY_600,
)

# Backwards compatibility alias
color = SEM

# Additional utility colors
WHITE = SURFACE
BLACK = ft.colors.BLACK
TRANSPARENT = ft.colors.TRANSPARENT
INVERSE_PRIMARY = ft.colors.INVERSE_PRIMARY
SURFACE_VARIANT = ft.colors.SURFACE_VARIANT

__all__ = [
    "PRIMARY_600",
    "BACKGROUND",
    "SURFACE",
    "TEXT",
    "TEXT_MUTED",
    "BORDER",
    "SUCCESS_BG",
    "SUCCESS_TEXT",
    "WARNING_BG",
    "WARNING_TEXT",
    "ERROR_BG",
    "ERROR_TEXT",
    "SEM",
    "color",
    "WHITE",
    "BLACK",
    "TRANSPARENT",
    "INVERSE_PRIMARY",
    "SURFACE_VARIANT",
]
