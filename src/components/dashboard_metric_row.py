import flet as ft
from components.dashboard import MetricCard
from theme.tokens import TOKENS as T


def make_metric_row(*, STATUS_INFO, values: dict, on_click):
    total_atas = values.get("total_atas", 0)
    total_value = values.get("valor_total", 0)
    vigentes = values.get("vigente", 0)
    a_vencer = values.get("a_vencer", 0)

    def pct_1(value: int, total: int) -> str:
        p = (value / total * 100) if total else 0
        return f"{p:.1f}%".replace(".", ",")

    cards = [
        MetricCard(ft.icons.DESCRIPTION_OUTLINED, "Total de Atas", str(total_atas), "cadastradas"),
        MetricCard(
            ft.icons.MONETIZATION_ON_OUTLINED,
            "Valor Total",
            f"R$ {total_value:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "em atas",
        ),
        MetricCard(
            ft.icons.CHECK_CIRCLE_OUTLINED,
            STATUS_INFO.get("vigente", {}).get("title", ""),
            str(vigentes),
            f"{pct_1(vigentes, total_atas)} do total",
        ),
        MetricCard(
            ft.icons.SCHEDULE_OUTLINED,
            STATUS_INFO.get("a_vencer", {}).get("title", ""),
            str(a_vencer),
            f"{pct_1(a_vencer, total_atas)} do total",
        ),
    ]

    for key, card in zip(["total", "valor_total", "vigente", "a_vencer"], cards):
        card.col = {"xs": 6, "md": 3}
        if key in STATUS_INFO and on_click:
            card.on_click = lambda e, s=key: on_click(s)

    return ft.ResponsiveRow(cards, columns=12, spacing=T.spacing.SPACE_4, run_spacing=T.spacing.SPACE_4)
