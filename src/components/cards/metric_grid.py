"""Grid of metric cards used on dashboard."""

from __future__ import annotations

from typing import Callable, Dict

import flet as ft

from theme.tokens import TOKENS as T
from .metric_card import MetricCard


class MetricGrid(ft.ResponsiveRow):
    """Responsive row containing status metric cards."""

    def __init__(
        self,
        status_info: Dict[str, Dict[str, str]],
        values: Dict[str, Dict[str, str]],
        on_click: Callable[[str], None],
    ) -> None:
        self._cards: Dict[str, MetricCard] = {}
        controls: list[ft.Control] = []
        for key, info in status_info.items():
            val = values.get(key, {"value": 0, "helper": ""})
            card = MetricCard(
                info["icon"],
                info["title"],
                str(val.get("value", 0)),
                val.get("helper", ""),
                on_click=lambda e, k=key: on_click(k),
            )
            card.col = {"xs": 6, "md": 3}
            self._cards[key] = card
            controls.append(card)
        super().__init__(
            controls,
            columns=12,
            spacing=T.spacing.SPACE_4,
            run_spacing=T.spacing.SPACE_4,
        )

    def update_data(self, values: Dict[str, Dict[str, str]]) -> None:
        """Update card values."""
        for key, card in self._cards.items():
            val = values.get(key, {"value": 0, "helper": ""})
            card.update_data(str(val.get("value", 0)), val.get("helper", ""))
        if self.page:
            self.update()


__all__ = ["MetricGrid"]
