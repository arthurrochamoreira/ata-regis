# Paleta única (sem modo claro/escuro)

# Base
PRIMARY = "#2563EB"      # Azul principal
BG_APP = "#F3F4F6"       # Fundo geral
SURFACE = "#FFFFFF"      # Cartões, modais, tabelas, inputs

# Texto
TEXT_PRIMARY = "#1F2937"
TEXT_SECONDARY = "#6B7280"

# Bordas/Divisórias
BORDER = "#D1D5DB"

# Estados de interação (derivados da primária)
PRIMARY_HOVER = "#1D4ED8"   # blue-700
PRIMARY_ACTIVE = "#1E40AF"  # blue-800
FOCUS_RING = "#93C5FD"      # blue-300 (se houver anel de foco)

# Status
SUCCESS_BG = "#DCFCE7"    # green-100
SUCCESS_TEXT = "#166534"  # green-800

WARNING_BG = "#FEF9C3"    # yellow-100
WARNING_TEXT = "#854D0E"  # yellow-800

ERROR_BG = "#FEE2E2"      # red-100
ERROR_TEXT = "#991B1B"    # red-800

from types import SimpleNamespace

color = SimpleNamespace(
    primary=PRIMARY,
    surface=SURFACE,
    background=BG_APP,
    text=TEXT_PRIMARY,
    muted=TEXT_SECONDARY,
    border=BORDER,
    error=ERROR_TEXT,
    focus_ring=FOCUS_RING,
)

__all__ = [name for name in globals().keys() if name.isupper()] + ["color"]
