import flet as ft
from typing import Callable, List, Dict, Tuple

from .theme.spacing import (
    SPACE_1,
    SPACE_2,
    SPACE_3,
    SPACE_4,
    SPACE_5,
    SPACE_6,
)
from .tokens import build_card, primary_button
from .theme.typography import (
    text,
    text_style,
    FONT_BOLD,
    TEXT_SM,
    TEXT_XL,
    LEADING_5,
    TRACKING_WIDER,
)
from .theme import colors
from utils.color_utils import get_status_colors

from models.ata import Ata
from utils.validators import Formatters
from utils.chart_utils import ChartUtils


STATUS_INFO = {
    "vigente": {
        "title": "Atas Vigentes",
        "filter": "Vigentes",
        "icon": ft.icons.CHECK_CIRCLE,
        "icon_color": colors.GREEN,
        "icon_bg": colors.GREEN_BG,
        "button_color": colors.GREEN,
    },
    "a_vencer": {
        "title": "Atas a Vencer",
        "filter": "A Vencer",
        "icon": ft.icons.WARNING_AMBER_ROUNDED,
        "icon_color": colors.YELLOW,
        "icon_bg": colors.YELLOW_BG,
        "button_color": colors.YELLOW,
    },
    "vencida": {
        "title": "Atas Vencidas",
        "filter": "Vencidas",
        "icon": ft.icons.CANCEL,
        "icon_color": colors.RED,
        "icon_bg": colors.RED_BG,
        "button_color": colors.RED,
    },
}


def build_header(
    nova_ata_cb: Callable,
    verificar_alertas_cb: Callable,
    relatorio_semanal_cb: Callable,
    relatorio_mensal_cb: Callable,
    testar_email_cb: Callable,
    status_cb: Callable,
    toggle_sidebar_cb: Callable,
) -> ft.AppBar:
    """Return AppBar with menu actions and new ata button."""
    actions_row = ft.Row(
        [
            ft.PopupMenuButton(
                icon=ft.icons.SETTINGS,
                tooltip="Ferramentas",
                items=[
                    ft.PopupMenuItem(text="🔍 Verificar Alertas", on_click=verificar_alertas_cb),
                    ft.PopupMenuItem(text="📊 Relatório Semanal", on_click=relatorio_semanal_cb),
                    ft.PopupMenuItem(text="📈 Relatório Mensal", on_click=relatorio_mensal_cb),
                    ft.PopupMenuItem(text="📧 Testar Email", on_click=testar_email_cb),
                    ft.PopupMenuItem(text="ℹ️ Status Sistema", on_click=status_cb),
                ],
            ),
            primary_button(
                "Nova Ata",
                icon=ft.icons.ADD,
                on_click=nova_ata_cb,
            ),
        ],
        spacing=SPACE_4,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    menu_button = ft.IconButton(
        icon=ft.icons.MENU,
        tooltip="Menu",
        on_click=toggle_sidebar_cb,
    )

    return ft.AppBar(
        leading=ft.Container(
            content=menu_button,
            padding=ft.padding.symmetric(horizontal=12),
            alignment=ft.alignment.center,
        ),
        leading_width=56,
        title=text(
            "Ata de Registro de Preços",
            size=TEXT_XL,
            weight=FONT_BOLD,
            line_height=LEADING_5,
            letter_spacing=TRACKING_WIDER,
        ),
        bgcolor=ft.colors.INVERSE_PRIMARY,
        actions=[
            ft.Container(
                content=actions_row,
                alignment=ft.alignment.center_right,
                padding=ft.padding.only(right=SPACE_5),
            )
        ],
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
            spacing=SPACE_1,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border=ft.border.all(1, colors.GREY_LIGHT),
        border_radius=8,
        bgcolor=colors.WHITE,
    )

    popup = ft.PopupMenuButton(content=button_content, items=items)

    container = ft.Container(
        content=popup,
        padding=ft.padding.symmetric(horizontal=SPACE_5, vertical=SPACE_5),
        expand=True,
    )

    return container, label_ref, checkboxes


def build_search(on_change: Callable, value: str = "") -> tuple[ft.Container, ft.TextField]:
    """Return a search container and field pre-populated with ``value``."""
    search_field = ft.TextField(
        hint_text="Buscar atas...",
        prefix_icon=ft.icons.SEARCH,
        on_change=on_change,
        value=value,
        expand=True,
        height=40,
        text_style=text_style(
            size=TEXT_SM,
            weight=ft.FontWeight.W_500,
            line_height=LEADING_5,
            letter_spacing=TRACKING_WIDER,
            color=colors.TEXT_DARK,
        ),
        hint_style=text_style(
            size=TEXT_SM,
            weight=ft.FontWeight.W_500,
            line_height=LEADING_5,
            letter_spacing=TRACKING_WIDER,
            color=colors.TEXT_DARK,
        ),
        border_radius=9999,
        border_color=colors.GREY_LIGHT,
        focused_border_color=colors.FOCUSED_BORDER,
        bgcolor=colors.WHITE,
        hover_color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
        content_padding=ft.padding.symmetric(horizontal=SPACE_4, vertical=0),
    )
    return (
        ft.Container(
            content=search_field,
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=SPACE_5, vertical=SPACE_5),
            margin=ft.margin.only(bottom=SPACE_6),
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
                color=colors.TEXT_SECONDARY,
                no_wrap=True,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(SPACE_4),
        )

    header_labels = ["Número", "Vigência", "Objeto", "Fornecedor", "Situação", "Ações"]

    # Relative width for columns: Número, Vigência, Objeto, Fornecedor, Situação, Ações
    column_expands = [1, 1, 2, 1, 1, 1]

    header_cells = [
        ft.Container(
                ft.Text(
                    lbl.upper(),
                    size=11,
                    weight=ft.FontWeight.W_600,
                    color=colors.TEXT_SECONDARY,
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
            spacing=SPACE_4,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(vertical=SPACE_4, horizontal=SPACE_4),
        bgcolor=colors.HEADER_BG,
        border=ft.border.only(bottom=ft.BorderSide(1, colors.GREY_LIGHT)),
    )

    rows: list[ft.Control] = []
    total = len(atas)
    for index, ata in enumerate(atas):
        data_formatada = Formatters.formatar_data_brasileira(ata.data_vigencia)
        text_cells = [
            ft.Text(
                ata.numero_ata,
                weight=ft.FontWeight.W_500,
                color=colors.TEXT_DARK,
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
            padding=ft.padding.symmetric(vertical=SPACE_1, horizontal=SPACE_3),
            bgcolor=badge_bg_color,
            border_radius=9999,
            alignment=ft.alignment.center,
        )

        actions = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.VISIBILITY,
                    tooltip="Visualizar",
                    on_click=lambda e, ata=ata: visualizar_cb(ata),
                    style=ft.ButtonStyle(
                        color={ft.MaterialState.HOVERED: colors.BLUE_HOVER, "": colors.TEXT_SECONDARY}
                    ),
                    icon_size=20,
                ),
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    tooltip="Editar",
                    on_click=lambda e, ata=ata: editar_cb(ata),
                    style=ft.ButtonStyle(
                        color={ft.MaterialState.HOVERED: colors.YELLOW, "": colors.TEXT_SECONDARY}
                    ),
                    icon_size=20,
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    tooltip="Excluir",
                    on_click=lambda e, ata=ata: excluir_cb(ata),
                    style=ft.ButtonStyle(
                        color={ft.MaterialState.HOVERED: colors.RED, "": colors.TEXT_SECONDARY}
                    ),
                    icon_size=20,
                ),
            ],
            spacing=SPACE_3,
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
                spacing=SPACE_3,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(SPACE_4),
            border=ft.border.only(bottom=ft.BorderSide(1, colors.GREY_LIGHT)) if index < total - 1 else None,
        )

        rows.append(row_container)

    body = ft.Column(rows, spacing=0)

    table = ft.Container(
        content=ft.Column([header_row, body], spacing=0),
        border=ft.border.all(1, colors.GREY_LIGHT),
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
                size=20,
            ),
            width=28,
            height=28,
            padding=ft.padding.all(SPACE_1),
            bgcolor=info["icon_bg"],
            border_radius=8,
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
                color=colors.TEXT_SECONDARY,
                no_wrap=True,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(SPACE_4),
            expand=True,
        )

    row = ft.ResponsiveRow(
        card_controls,
        columns=12,
        alignment=ft.MainAxisAlignment.START,
        spacing=SPACE_5,
        run_spacing=SPACE_5,
        expand=True,
    )

    container = ft.Container(
        content=ft.Column(
            [row],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        alignment=ft.alignment.top_left,
        padding=ft.padding.only(left=SPACE_5, right=SPACE_5, top=SPACE_5, bottom=SPACE_5),
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
                        color=colors.RED if ata.dias_restantes <= 30 else colors.ORANGE,
                    ),
                ], spacing=SPACE_1),
                ft.Row([
                    ft.IconButton(icon=ft.icons.VISIBILITY, tooltip="Visualizar", on_click=lambda e, ata=ata: visualizar_cb(ata)),
                    ft.IconButton(icon=ft.icons.EMAIL, tooltip="Enviar Alerta", on_click=lambda e, ata=ata: alerta_cb(ata)),
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(SPACE_3),
            margin=ft.margin.only(bottom=SPACE_2),
            border=ft.border.all(1, colors.ORANGE),
            border_radius=8,
            bgcolor=colors.ORANGE_BG,
        )
        items.append(item)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "🔔 Atas Próximas do Vencimento",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Column(items, spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ],
            spacing=SPACE_3,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(horizontal=SPACE_5, vertical=SPACE_4),
        border=ft.border.all(1, colors.OUTLINE),
        border_radius=8,
    )


def build_stats_panel(ata_service) -> ft.Container:
    stats = ata_service.get_estatisticas()
    atas = ata_service.listar_todas()
    atas_vencimento = ata_service.get_atas_vencimento_proximo()
    total_value = sum(ata.valor_total for ata in atas)
    summary_cards = ChartUtils.create_summary_cards(stats, total_value)
    pie_chart = ChartUtils.create_status_pie_chart(stats)
    legend = ChartUtils.create_status_legend(stats)
    urgency_indicator = ChartUtils.create_urgency_indicator(atas_vencimento)
    value_chart = ChartUtils.create_value_chart(atas)
    monthly_chart = ChartUtils.create_monthly_chart(atas)

    chart_left = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "📊 Situação das Atas",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    [pie_chart, legend],
                    spacing=SPACE_6,
                    alignment=ft.MainAxisAlignment.START,
                ),
                value_chart,
            ],
            spacing=SPACE_4,
        ),
        padding=ft.padding.all(SPACE_4),
        border=ft.border.all(1, colors.OUTLINE),
        border_radius=8,
        expand=True,
    )
    chart_left.col = {"xs": 12, "lg": 8}
    chart_right = ft.Container(content=monthly_chart, width=360)
    chart_right.col = {"xs": 12, "lg": 4}
    charts_section = ft.ResponsiveRow(
        [chart_left, chart_right],
        columns=12,
        spacing=SPACE_4,
        run_spacing=SPACE_4,
    )

    return ft.Container(
        content=ft.Column(
            [urgency_indicator, summary_cards, charts_section], spacing=SPACE_4
        ),
        padding=ft.padding.symmetric(horizontal=SPACE_5),
        margin=ft.margin.only(bottom=SPACE_5),
    )
