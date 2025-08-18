# Responsiveness utilities and breakpoints

BREAKPOINT_SM = 640
BREAKPOINT_MD = 1024
BREAKPOINT_LG = 1280

# maps breakpoints to paddings and font multipliers using design tokens
from ui.theme.tokens import TOKENS as T

PADDINGS = {
    "xs": T.spacing.SPACE_2,
    "md": T.spacing.SPACE_4,
    "lg": T.spacing.SPACE_5,
}

FONT_SCALE = {
    "xs": 0.9,
    "md": 1.0,
    "lg": 1.1,
}

def get_breakpoint(width: int) -> str:
    """Return breakpoint name based on ``width``."""
    if width < BREAKPOINT_SM:
        return "xs"
    if width < BREAKPOINT_MD:
        return "md"
    return "lg"


def get_padding(width: int) -> int:
    bp = get_breakpoint(width)
    return PADDINGS.get(bp, T.spacing.SPACE_4)


def get_font_size(width: int, base: int) -> int:
    bp = get_breakpoint(width)
    scale = FONT_SCALE.get(bp, 1)
    return int(base * scale)

# Checklist responsividade:
# - breakpoints aplicados com get_breakpoint
# - componentes expansíveis usando col/expand
# - fontes e paddings dinâmicos via helpers
# - overflow horizontal evitado
