"""Motion tokens: durations and easing curves."""

DURATION_FAST = 120  # ms
DURATION_BASE = 200  # ms
DURATION_SLOW = 300  # ms

EASING = "cubic-bezier(0.2,0,0,1)"

# Diretriz: use DURATION_FAST para hover/focus, DURATION_BASE para transições
# padrão e DURATION_SLOW para expansões mais longas.

__all__ = ["DURATION_FAST", "DURATION_BASE", "DURATION_SLOW", "EASING"]
