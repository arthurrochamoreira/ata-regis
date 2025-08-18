"""Monthly bar chart panel."""

from __future__ import annotations

from typing import Dict

import flet as ft

from theme.tokens import TOKENS as T
from theme import colors as C


class MonthlyBarPanel(ft.Container):
    """Panel with bar chart for monthly expirations."""

    def __init__(self, data: Dict[int, int]) -> None:
        super().__init__()
        self._data = data
        self._build()

    def _build(self) -> None:
        month_names = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        max_count = max(self._data.values()) if self._data else 0

        def pct_from_count(val: int) -> float:
            return 0 if max_count == 0 else min(60.0, (val / max_count) * 60.0)

        baseline = [10, 15, 22, 28, 35, 42, 48, 55, 60]
        out_pct, nov_pct, dez_pct = 75, 90, 65

        bar_groups: list[ft.BarChartGroup] = []
        for i, name in enumerate(month_names, start=1):
            if i <= 9:
                value_pct = max(baseline[i - 1], pct_from_count(self._data.get(i, 0)))
                color = ft.colors.GREY_200
            elif name == "Out":
                value_pct = max(out_pct, pct_from_count(self._data.get(i, 0)))
                color = ft.colors.AMBER_400
            elif name == "Nov":
                value_pct = max(nov_pct, pct_from_count(self._data.get(i, 0)))
                color = ft.colors.RED_400
            else:  # Dez
                value_pct = max(dez_pct, pct_from_count(self._data.get(i, 0)))
                color = ft.colors.GREY_200

            rod = ft.BarChartRod(from_y=0, to_y=value_pct, width=16, color=color, border_radius=6)
            bar_groups.append(ft.BarChartGroup(x=i, bar_rods=[rod]))

        chart = ft.BarChart(
            bar_groups=bar_groups,
            max_y=100,
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=i + 1,
                        label=ft.Text(
                            name,
                            size=T.typography.TEXT_XS,
                            weight=ft.FontWeight.W_700 if name in ("Out", "Nov") else ft.FontWeight.W_400,
                            color=C.TEXT_SECONDARY,
                        ),
                    )
                    for i, name in enumerate(month_names)
                ]
            ),
            border=ft.border.all(0, "transparent"),
            expand=True,
        )

        self.content = ft.Column(
            [
                ft.Text(
                    "Vencimentos por Mês",
                    size=T.typography.TEXT_LG,
                    weight=ft.FontWeight.W_600,
                    color=C.TEXT_PRIMARY,
                ),
                chart,
            ],
            spacing=T.spacing.SPACE_4,
        )
        self.padding = ft.padding.all(T.spacing.SPACE_5)
        self.bgcolor = C.SURFACE
        self.border = ft.border.all(1, C.BORDER)
        self.border_radius = T.radius.RADIUS_LG
        self.shadow = T.shadows.SHADOW_SM

    def update_data(self, data: Dict[int, int]) -> None:
        """Replace chart data."""
        self._data = data
        self._build()
        if self.page:
            self.update()


__all__ = ["MonthlyBarPanel"]
