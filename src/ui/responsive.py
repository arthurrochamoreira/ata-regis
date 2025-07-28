# Responsiveness utilities and breakpoints

BREAKPOINT_SM = 640
BREAKPOINT_MD = 1024
BREAKPOINT_LG = 1280

# maps breakpoints to paddings and font multipliers
PADDINGS = {
    "xs": 8,
    "md": 16,
    "lg": 24,
}

FONT_SCALE = {
    "xs": 0.9,
    "md": 1.0,
    "lg": 1.1,
}

# helpers to expose intuitive API
def font_size_for(width: int, base: int) -> int:
    """Return scaled font size for given ``width``."""  # responsive font
    return get_font_size(width, base)


def padding_for(width: int) -> int:
    """Return padding size for given ``width``."""  # responsive padding
    return get_padding(width)

def get_breakpoint(width: int) -> str:
    """Return breakpoint name based on ``width``."""
    if width < BREAKPOINT_SM:
        return "xs"
    if width < BREAKPOINT_MD:
        return "md"
    return "lg"


def get_padding(width: int) -> int:
    bp = get_breakpoint(width)
    return PADDINGS.get(bp, 16)


def get_font_size(width: int, base: int) -> int:
    bp = get_breakpoint(width)
    scale = FONT_SCALE.get(bp, 1)
    return int(base * scale)

# Checklist responsividade:
# - breakpoints aplicados com get_breakpoint
# - componentes expansíveis usando col/expand
# - fontes e paddings dinâmicos via helpers
# - overflow horizontal evitado
# - max_lines/overflow nos textos críticos
# - fontes/paddings por breakpoint
# - sem overflow horizontal
# - DataTable e badges tratados
