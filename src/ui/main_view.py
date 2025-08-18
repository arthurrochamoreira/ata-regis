"""Main view composition using reusable components."""

from __future__ import annotations

import flet as ft

from theme.tokens import TOKENS as T
from components.cards.metric_grid import MetricGrid
from components.charts.donut_panel import DonutPanel
from components.charts.monthly_bar_panel import MonthlyBarPanel
from components.feedback.alert_banner import AlertBanner
from .dashboard_tokens import STATUS_INFO


class MainView(ft.Column):
    """Compose dashboard layout."""

    def __init__(self, controller=None) -> None:
        super().__init__(spacing=T.spacing.SPACE_5, expand=True)
        self._c = controller
        self.alert = AlertBanner(ft.icons.WARNING_AMBER_ROUNDED, "Atenção", "")
        metrics = controller.metrics() if controller else {}
        grid_values = {k: metrics.get(k, {"value": 0, "helper": ""}) for k in STATUS_INFO.keys()}
        self.metric_grid = MetricGrid(STATUS_INFO, grid_values, self._on_status_click)
        self.donut_panel = DonutPanel(controller.donut_data() if controller else {})
        self.monthly_panel = MonthlyBarPanel(controller.monthly_data() if controller else {})
        charts_row = ft.ResponsiveRow(
            [self.donut_panel, self.monthly_panel],
            columns=12,
            spacing=T.spacing.SPACE_4,
            run_spacing=T.spacing.SPACE_4,
            expand=True,
        )
        self.controls = [self.alert, self.metric_grid, charts_row]
        self.padding = ft.padding.symmetric(horizontal=T.spacing.SPACE_5, vertical=T.spacing.SPACE_5)

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def _on_status_click(self, key: str) -> None:
        if self._c:
            self._c.filter_by_status(key)

    def refresh(self) -> None:
        """Refresh dynamic widgets with new data from controller."""
        if not self._c:
            return
        metrics = self._c.metrics()
        grid_values = {k: metrics.get(k, {"value": 0, "helper": ""}) for k in STATUS_INFO.keys()}
        self.metric_grid.update_data(grid_values)
        self.donut_panel.update_data(self._c.donut_data())
        self.monthly_panel.update_data(self._c.monthly_data())
        expiring = metrics.get("expiring", 0)
        self.alert.subtitle.value = f"Você possui {expiring} ata(s) vencendo em 90 dias ou menos."
        if self.page:
            self.update()


__all__ = ["MainView"]
