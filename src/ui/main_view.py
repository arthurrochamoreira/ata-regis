import flet as ft
from flet import colors as fcolors
from typing import Callable, List, Dict, Tuple

from theme.tokens import TOKENS as T
from theme import colors as C
from components import (
    PrimaryButton,
    IconAction,
    TextInput,
    AlertBanner,
    MetricCard,
    DonutStatus,
    MonthlyBarChart,
)
from .tokens import build_card
from theme.typography import text, text_style
from utils.color_utils import get_status_colors

from models.ata import Ata
from utils.validators import Formatters


STATUS_INFO = {
    "vigente": {
        "title": "Atas Vigentes",
        "filter": "Vigentes",
        "icon": ft.icons.CHECK_CIRCLE,
        "icon_color": C.SUCCESS_TEXT,
        "icon_bg": C.SUCCESS_BG,
        "button_color": C.SUCCESS_TEXT,
    },
    "a_vencer": {
        "title": "Atas a Vencer",
        "filter": "A Vencer",
        "icon": ft.icons.WARNING_AMBER_ROUNDED,
        "icon_color": C.WARNING_TEXT,
        "icon_bg": C.WARNING_BG,
        "button_color": C.WARNING_TEXT,
    },
    "vencida": {
        "title": "Atas Vencidas",
        "filter": "Vencidas",
        "icon": ft.icons.CANCEL,
        "icon_color": C.ERROR_TEXT,
        "icon_bg": C.ERROR_BG,
        "button_color": C.ERROR_TEXT,
    },
}


def build_header(
    nova_ata_cb: Callable,
) -> ft.AppBar:
    """Return AppBar with only the new ata button."""
    appbar_height = T.sizes.APPBAR_HEIGHT

    actions_row = ft.Row(
        [
            PrimaryButton(
                "Nova Ata",
                icon=ft.icons.ADD,
                on_click=nova_ata_cb,
            ),
        ],
        spacing=T.spacing.SPACE_4,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.AppBar(
        leading=ft.Icon(ft.icons.DESCRIPTION_OUTLINED),
        leading_width=T.sizes.APPBAR_LEADING_W,
        title=text(
            "Ata de Registro de Preços",
            size=T.typography.TEXT_XL,
            weight=T.typography.FONT_BOLD,
            line_height=T.typography.LEADING_5,
            letter_spacing=T.typography.TRACKING_WIDER,
        ),
        bgcolor=C.PRIMARY,
        actions=[
            ft.Container(
                content=actions_row,
                alignment=ft.alignment.center_right,
                padding=ft.padding.only(right=T.spacing.SPACE_5),
            )
        ],
        toolbar_height=appbar_height,
    )


def build_filters(
    filtros_ativos: List[str],
    toggle_cb: Callable[[str, bool], None],
) -> Tuple[ft.Container, ft.Text, Dict[str, ft.Checkbox]]:
    """Return filter dropdown and references for external state handling.

    ``toggle_cb`` is called whenever a checkbox changes and receives the key
    and the new ``bool`` value. The function returns a tuple containing the
    filter container, the label ``ft.Text`` to be updated externally and a
    dictionary mapping filter keys to their respective ``ft.Checkbox``
    controls.
    """

    active = set(filtros_ativos or [])

    label_ref = ft.Text("Filtro")
    checkboxes: Dict[str, ft.Checkbox] = {}

    items: List[ft.PopupMenuItem] = []

    def add_checkbox(key: str, text_label: str) -> None:
        cb = ft.Checkbox(
            label=text_label,
            value=key in active,
            on_change=lambda e, k=key: toggle_cb(k, e.control.value),
        )
        checkboxes[key] = cb
        items.append(ft.PopupMenuItem(content=cb))

    add_checkbox("todos", "Todas as Atas")
    for key in ["vigente", "a_vencer", "vencida"]:
        info = STATUS_INFO[key]
        add_checkbox(key, info["title"])

    button_content = ft.Container(
        content=ft.Row(
            [label_ref, ft.Icon(ft.icons.ARROW_DROP_DOWN)],
            spacing=T.spacing.SPACE_1,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(
            horizontal=T.spacing.SPACE_3, vertical=T.spacing.SPACE_2
        ),
        border=ft.border.all(1, C.BORDER),
        border_radius=T.radius.RADIUS_MD,
        bgcolor=C.SURFACE,
    )

    popup = ft.PopupMenuButton(content=button_content, items=items)

    container = ft.Container(
        content=popup,
        padding=ft.padding.symmetric(horizontal=T.spacing.SPACE_5, vertical=T.spacing.SPACE_5),
        expand=True,
    )

    return container, label_ref, checkboxes


def build_search(on_change: Callable, value: str = "") -> tuple[ft.Container, ft.TextField]:
    """Return a search container and field pre-populated with ``value``."""
    search_field = TextInput(
        hint_text="Buscar atas...",
        prefix_icon=ft.icons.SEARCH,
        on_change=on_change,
        value=value,
        expand=True,
        height=T.sizes.SEARCH_FIELD_H,
        text_style=text_style(
            size=T.typography.TEXT_SM,
            weight=ft.FontWeight.W_500,
            line_height=T.typography.LEADING_5,
            letter_spacing=T.typography.TRACKING_WIDER,
            color=C.TEXT_PRIMARY,
        ),
        hint_style=text_style(
            size=T.typography.TEXT_SM,
            weight=ft.FontWeight.W_500,
            line_height=T.typography.LEADING_5,
            letter_spacing=T.typography.TRACKING_WIDER,
            color=C.TEXT_PRIMARY,
        ),
        border_radius=T.radius.RADIUS_FULL,
        border_color=C.BORDER,
        focused_border_color=C.PRIMARY,
        bgcolor=C.SURFACE,
        hover_color=fcolors.with_opacity(0.08, C.TEXT_PRIMARY),
        content_padding=ft.padding.symmetric(horizontal=T.spacing.SPACE_4, vertical=0),
    )
    return (
        ft.Container(
            content=search_field,
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=T.spacing.SPACE_5, vertical=T.spacing.SPACE_5),
            margin=ft.margin.only(bottom=T.spacing.SPACE_6),
            expand=True,
        ),
        search_field,
    )


def build_data_table(
    atas: List[Ata],
    visualizar_cb: Callable[[Ata], None],
    editar_cb: Callable[[Ata], None],
    excluir_cb: Callable[[Ata], None],
    status: str,
) -> ft.Column:
    """Return custom table for a list of atas respecting design specs."""
    if not atas:
        return ft.Container(
            content=ft.Text(
                "Nenhuma ata encontrada",
                color=C.TEXT_SECONDARY,
                no_wrap=True,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(T.spacing.SPACE_4),
        )

    header_labels = ["Número", "Vigência", "Objeto", "Fornecedor", "Situação", "Ações"]

    # Relative width for columns: Número, Vigência, Objeto, Fornecedor, Situação, Ações
    column_expands = [1, 1, 2, 1, 1, 1]

    header_cells = [
        ft.Container(
                ft.Text(
                    lbl.upper(),
                    size=T.typography.TEXT_XS,
                    weight=ft.FontWeight.W_600,
                    color=C.TEXT_SECONDARY,
                    no_wrap=True,
                    text_align=ft.TextAlign.CENTER,
                ),
            expand=exp,
            alignment=ft.alignment.center,
        )
        for lbl, exp in zip(header_labels, column_expands)
    ]
    header_row = ft.Container(
        content=ft.Row(
            header_cells,
            spacing=T.spacing.SPACE_4,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(vertical=T.spacing.SPACE_4, horizontal=T.spacing.SPACE_4),
        bgcolor=C.BG_APP,
        border=ft.border.only(bottom=ft.BorderSide(1, C.BORDER)),
    )

    rows: list[ft.Control] = []
    total = len(atas)
    for index, ata in enumerate(atas):
        data_formatada = Formatters.formatar_data_brasileira(ata.data_vigencia)
        text_cells = [
            ft.Text(
                ata.numero_ata,
                weight=ft.FontWeight.W_500,
                color=C.TEXT_PRIMARY,
                max_lines=1,
                no_wrap=True,
                overflow=ft.TextOverflow.ELLIPSIS,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                data_formatada,
                max_lines=1,
                no_wrap=True,
                overflow=ft.TextOverflow.ELLIPSIS,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                ata.objeto,
                max_lines=1,
                no_wrap=True,
                overflow=ft.TextOverflow.ELLIPSIS,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                ata.fornecedor,
                max_lines=1,
                no_wrap=True,
                overflow=ft.TextOverflow.ELLIPSIS,
                text_align=ft.TextAlign.CENTER,
            ),
        ]
        badge_text_color, badge_bg_color = get_status_colors(ata.status)
        badge = ft.Container(
            ft.Text(
                ata.status.replace("_", " ").title(),
                size=12,
                weight=ft.FontWeight.W_500,
                color=badge_text_color,
                no_wrap=True,
                text_align=ft.TextAlign.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=T.spacing.SPACE_1, horizontal=T.spacing.SPACE_3),
            bgcolor=badge_bg_color,
            border_radius=T.radius.RADIUS_FULL,
            alignment=ft.alignment.center,
        )

        actions = ft.Row(
            [
                IconAction(
                    icon=ft.icons.VISIBILITY,
                    tooltip="Visualizar",
                    on_click=lambda e, ata=ata: visualizar_cb(ata),
                    hover_color=C.PRIMARY_HOVER,
                    size="sm",
                ),
                IconAction(
                    icon=ft.icons.EDIT,
                    tooltip="Editar",
                    on_click=lambda e, ata=ata: editar_cb(ata),
                    hover_color=C.WARNING_TEXT,
                    size="sm",
                ),
                IconAction(
                    icon=ft.icons.DELETE,
                    tooltip="Excluir",
                    on_click=lambda e, ata=ata: excluir_cb(ata),
                    hover_color=C.ERROR_TEXT,
                    size="sm",
                ),
            ],
            spacing=T.spacing.SPACE_3,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        cells = [
            ft.Container(content, expand=exp, alignment=ft.alignment.center)
            for content, exp in zip(
                [*text_cells, badge, actions], column_expands
            )
        ]

        row_container = ft.Container(
            content=ft.Row(
                cells,
                spacing=T.spacing.SPACE_3,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(T.spacing.SPACE_4),
            border=ft.border.only(bottom=ft.BorderSide(1, C.BORDER)) if index < total - 1 else None,
        )

        rows.append(row_container)

    body = ft.Column(rows, spacing=0)

    table = ft.Container(
        content=ft.Column([header_row, body], spacing=0),
        border=ft.border.all(1, C.BORDER),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    return table


def build_grouped_data_tables(
    atas: List[Ata],
    visualizar_cb: Callable[[Ata], None],
    editar_cb: Callable[[Ata], None],
    excluir_cb: Callable[[Ata], None],
    filtros: List[str] | None = None,
) -> ft.Container:
    """Return layout with status cards respecting ``filtros``.

    When ``filtros`` contains specific status values, only those cards are
    returned. If ``filtros`` is ``None`` or contains ``"todos"``, all status
    cards are displayed. Cards are always arranged vertically.
    """

    groups: dict[str, list[Ata]] = {key: [] for key in STATUS_INFO}
    for ata in atas:
        groups.setdefault(ata.status, []).append(ata)

    # ``todos`` deve exibir todos os tipos de status disponíveis
    if not filtros or "todos" in filtros:
        statuses = list(STATUS_INFO.keys())
    else:
        statuses = filtros

    card_controls: list[ft.Control] = []
    for status in statuses:
        atas_status = groups.get(status, [])

        info = STATUS_INFO[status]

        icon = ft.Container(
            content=ft.Icon(
                info["icon"],
                color=info["icon_color"],
                size=T.sizes.ICON_SM,
            ),
            width=T.sizes.ICON_BUTTON,
            height=T.sizes.ICON_BUTTON,
            padding=ft.padding.all(T.spacing.SPACE_1),
            bgcolor=info["icon_bg"],
            border_radius=T.radius.RADIUS_MD,
        )

        table = build_data_table(
            atas_status,
            visualizar_cb,
            editar_cb,
            excluir_cb,
            status,
        )

        card = build_card(info["title"], icon, table)
        card.expand = True
        card_controls.append(card)

    if not card_controls:
        return ft.Container(
            content=ft.Text(
                "Nenhuma ata encontrada",
                color=C.TEXT_SECONDARY,
                no_wrap=True,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(T.spacing.SPACE_4),
            expand=True,
        )

    row = ft.ResponsiveRow(
        card_controls,
        columns=12,
        alignment=ft.MainAxisAlignment.START,
        spacing=T.spacing.SPACE_5,
        run_spacing=T.spacing.SPACE_5,
        expand=True,
    )

    container = ft.Container(
        content=ft.Column(
            [row],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        alignment=ft.alignment.top_left,
        padding=ft.padding.only(left=T.spacing.SPACE_5, right=T.spacing.SPACE_5, top=T.spacing.SPACE_5, bottom=T.spacing.SPACE_5),
        expand=True,
    )
    return container


def build_atas_vencimento(
    atas_vencimento: List[Ata],
    visualizar_cb: Callable[[Ata], None],
    alerta_cb: Callable[[Ata], None],
) -> ft.Container:
    if not atas_vencimento:
        return ft.Container()

    items = []
    for ata in atas_vencimento:
        data_formatada = Formatters.formatar_data_brasileira(ata.data_vigencia)
        item = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(f"Ata: {ata.numero_ata}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Vencimento: {data_formatada}"),
                    ft.Text(
                        f"Faltam {ata.dias_restantes} dias",
                        color=C.ERROR_TEXT if ata.dias_restantes <= 30 else C.WARNING_TEXT,
                    ),
                ], spacing=T.spacing.SPACE_1),
                ft.Row([
                    IconAction(
                        icon=ft.icons.VISIBILITY,
                        tooltip="Visualizar",
                        on_click=lambda e, ata=ata: visualizar_cb(ata),
                        hover_color=C.PRIMARY_HOVER,
                        size="sm",
                    ),
                    IconAction(
                        icon=ft.icons.EMAIL,
                        tooltip="Enviar Alerta",
                        on_click=lambda e, ata=ata: alerta_cb(ata),
                        hover_color=C.WARNING_TEXT,
                        size="sm",
                    ),
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(T.spacing.SPACE_3),
            margin=ft.margin.only(bottom=T.spacing.SPACE_2),
            border=ft.border.all(1, C.WARNING_TEXT),
            border_radius=T.radius.RADIUS_MD,
            bgcolor=C.WARNING_BG,
        )
        items.append(item)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "🔔 Atas Próximas do Vencimento",
                    size=T.typography.TEXT_BASE,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Column(items, spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ],
            spacing=T.spacing.SPACE_3,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(horizontal=T.spacing.SPACE_5, vertical=T.spacing.SPACE_4),
        border=ft.border.all(1, C.BORDER),
        border_radius=T.radius.RADIUS_MD,
    )


def build_stats_panel(ata_service) -> ft.Container:
    stats = ata_service.get_estatisticas()
    atas = ata_service.listar_todas()
    atas_vencimento = ata_service.get_atas_vencimento_proximo()

    total_value = sum(ata.valor_total for ata in atas)
    total_atas = sum(stats.values())
    vigentes = stats.get("vigente", 0)
    a_vencer = stats.get("a_vencer", 0)

    banner = AlertBanner(
        icon=ft.icons.WARNING_AMBER_ROUNDED,
        title="Atenção",
        subtitle=f"Você possui {len(atas_vencimento)} ata(s) vencendo em 90 dias ou menos.",
    )

    cards = [
        MetricCard(
            ft.icons.DESCRIPTION_OUTLINED,
            "Total de Atas",
            str(total_atas),
            "cadastradas",
        ),
        MetricCard(
            ft.icons.MONETIZATION_ON_OUTLINED,
            "Valor Total",
            f"R$ {total_value:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "em atas",
        ),
        MetricCard(
            ft.icons.CHECK_CIRCLE_OUTLINED,
            "Vigentes",
            str(vigentes),
            f"{(vigentes / total_atas * 100) if total_atas else 0:.0f}%",
        ),
        MetricCard(
            ft.icons.SCHEDULE_OUTLINED,
            "A Vencer",
            str(a_vencer),
            f"{(a_vencer / total_atas * 100) if total_atas else 0:.0f}%",
        ),
    ]
    for card in cards:
        card.col = {"xs": 6, "md": 3}

    # Donut data and chart
    donut = DonutStatus(
        {
            "vigente": vigentes,
            "a_vencer": a_vencer,
            "vencida": stats.get("vencida", 0),
        }
    )
    donut.col = {"xs": 12, "md": 6}

    # Monthly bar chart data
    from datetime import date

    current_year = date.today().year
    monthly_counts: dict[int, int] = {i: 0 for i in range(1, 13)}
    for ata in atas:
        if ata.data_vigencia.year == current_year:
            monthly_counts[ata.data_vigencia.month] += 1

    bars = MonthlyBarChart(monthly_counts)
    bars.col = {"xs": 12, "md": 6}

    cards_row = ft.ResponsiveRow(
        cards,
        columns=12,
        spacing=T.spacing.SPACE_4,
        run_spacing=T.spacing.SPACE_4,
    )

    charts_row = ft.ResponsiveRow(
        [donut, bars],
        columns=12,
        spacing=T.spacing.SPACE_4,
        run_spacing=T.spacing.SPACE_4,
    )

    return ft.Container(
        content=ft.Column(
            [banner, cards_row, charts_row], spacing=T.spacing.SPACE_5
        ),
        padding=ft.padding.symmetric(horizontal=T.spacing.SPACE_5),
        margin=ft.margin.only(bottom=T.spacing.SPACE_5),
    )
