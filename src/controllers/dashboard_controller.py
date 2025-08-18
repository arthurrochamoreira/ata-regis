"""Dashboard controller coordinating services and view."""

from __future__ import annotations

from typing import Dict, Optional
from datetime import date

from services.ata_service import AtaService


class DashboardController:
    """Encapsulates dashboard state and actions."""

    def __init__(self, view, ata_service: AtaService) -> None:
        self.view = view
        self.ata_service = ata_service
        self.state: Dict[str, Optional[str]] = {
            "q": "",
            "sort": "recentes",
            "status": None,
        }

    # ------------------------------------------------------------------
    # Data providers
    # ------------------------------------------------------------------
    def metrics(self) -> Dict[str, Dict[str, str]]:
        """Return metrics including totals and status counts."""
        atas = self.ata_service.listar_todas()
        total = len(atas)
        total_value = sum(item.valor_total for ata in atas for item in ata.itens)
        stats = self.ata_service.get_estatisticas()

        def pct(val: int) -> str:
            return f"{(val / total * 100 if total else 0):.1f}%".replace(".", ",")

        metrics = {
            "total": {"value": total, "helper": "cadastradas"},
            "valor_total": {
                "value": f"R$ {total_value:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "helper": "em atas",
            },
            "vigente": {"value": stats.get("vigente", 0), "helper": f"{pct(stats.get('vigente', 0))} do total"},
            "a_vencer": {"value": stats.get("a_vencer", 0), "helper": f"{pct(stats.get('a_vencer', 0))} do total"},
            "vencida": {"value": stats.get("vencida", 0), "helper": f"{pct(stats.get('vencida', 0))} do total"},
            "expiring": self.ata_service.get_atas_vencimento_proximo(),
        }
        metrics["expiring"] = len(metrics["expiring"])  # convert to count
        return metrics

    def donut_data(self) -> Dict[str, int]:
        """Return counts per status."""
        return self.ata_service.get_estatisticas()

    def monthly_data(self) -> Dict[int, int]:
        """Return monthly counts for current year."""
        current_year = date.today().year
        counts = {i: 0 for i in range(1, 13)}
        for ata in self.ata_service.listar_todas():
            if ata.data_vigencia.year == current_year:
                counts[ata.data_vigencia.month] += 1
        return counts

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def apply_search(self, q: str) -> None:
        self.state["q"] = q
        self.view.refresh()

    def clear_filters(self) -> None:
        self.state = {"q": "", "sort": "recentes", "status": None}
        self.view.refresh()

    def set_sort(self, sort: str) -> None:
        self.state["sort"] = sort
        self.view.refresh()

    def filter_by_status(self, key: str) -> None:
        self.state["status"] = key
        self.view.refresh()


__all__ = ["DashboardController"]
