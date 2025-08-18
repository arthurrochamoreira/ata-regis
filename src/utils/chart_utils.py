import flet as ft
from typing import List, Dict, Any, Tuple
from datetime import date, datetime, timedelta

from models.ata import Ata
from theme.tokens import TOKENS as T
from theme import colors as C

S, R = T.spacing, T.radius

class ChartUtils:
    """Utilitários para criação de gráficos e visualizações"""
    
    @staticmethod
    def create_status_pie_chart(stats: Dict[str, int], width: int = 200, height: int = 200) -> ft.PieChart:
        """Cria gráfico de pizza para status das atas"""
        total = sum(stats.values())
        
        if total == 0:
            return ft.Container(
                content=ft.Text("Nenhuma ata cadastrada"),
                width=width,
                height=height,
                alignment=ft.alignment.center
            )
        
        # Cores para cada status
        colors = {
            "vigente": C.SUCCESS_TEXT,
            "a_vencer": C.WARNING_TEXT,
            "vencida": C.ERROR_TEXT,
        }
        
        # Cria seções do gráfico
        sections = []
        for status, count in stats.items():
            if count > 0:
                percentage = (count / total) * 100
                sections.append(
                    ft.PieChartSection(
                        value=count,
                        title=f"{percentage:.1f}%",
                        color=colors[status],
                        radius=60,
                        title_style=ft.TextStyle(
                            size=12,
                            color="#FFFFFF",
                            weight=ft.FontWeight.BOLD,
                        ),
                    )
                )

        return ft.PieChart(
            sections=sections,
            sections_space=4,
            center_space_radius=40,
            width=width,
            height=height,
        )
    
    @staticmethod
    def create_status_legend(stats: Dict[str, int]) -> ft.Column:
        """Cria legenda para o gráfico de status"""
        total = sum(stats.values())
        
        if total == 0:
            return ft.Column([ft.Text("Nenhuma ata cadastrada")])
        
        # Ícones e cores para cada status
        status_info = {
            "vigente": {"icon": "✅", "color": C.SUCCESS_TEXT, "label": "Vigentes"},
            "a_vencer": {"icon": "⚠️", "color": C.WARNING_TEXT, "label": "A Vencer"},
            "vencida": {"icon": "❌", "color": C.ERROR_TEXT, "label": "Vencidas"},
        }
        
        legend_items = []
        for status, count in stats.items():
            info = status_info[status]
            percentage = (count / total * 100) if total > 0 else 0
            
            item = ft.Row([
                ft.Container(
                    width=S.SPACE_4,
                    height=S.SPACE_4,
                    bgcolor=info["color"],
                    border_radius=R.RADIUS_XS,
                ),
                ft.Text(f"{info['icon']} {info['label']}: {count} ({percentage:.1f}%)")
            ], spacing=S.SPACE_2)
            
            legend_items.append(item)
        
        return ft.Column(legend_items, spacing=S.SPACE_2)
    
    @staticmethod
    def create_monthly_chart(atas: List[Ata]) -> ft.Container:
        """Cria gráfico de barras para vencimentos por mês"""
        # Agrupa atas por mês de vencimento
        monthly_data = {}
        current_year = date.today().year
        
        # Inicializa todos os meses do ano atual
        for month in range(1, 13):
            month_name = datetime(current_year, month, 1).strftime("%b")
            monthly_data[month_name] = {"vigente": 0, "a_vencer": 0, "vencida": 0}
        
        # Conta atas por mês
        for ata in atas:
            if ata.data_vigencia.year == current_year:
                month_name = ata.data_vigencia.strftime("%b")
                if month_name in monthly_data:
                    monthly_data[month_name][ata.status] += 1
        
        # Cria barras para cada mês
        bars = []
        max_value = max(sum(data.values()) for data in monthly_data.values()) if monthly_data else 1
        
        for month, data in monthly_data.items():
            total = sum(data.values())
            height_ratio = (total / max_value) if max_value > 0 else 0
            bar_height = max(20, height_ratio * 100)  # Altura mínima de 20px
            
            # Cor da barra baseada no status predominante
            if data["vencida"] > 0:
                bar_color = C.ERROR_BG
            elif data["a_vencer"] > 0:
                bar_color = C.WARNING_BG
            else:
                bar_color = C.SUCCESS_BG
            
            bar = ft.Container(
                content=ft.Column([
                    ft.Container(
                        width=30,
                        height=bar_height,
                        bgcolor=bar_color,
                        border_radius=R.RADIUS_XS,
                        tooltip=f"{month}: {total} atas"
                    ),
                    ft.Text(month, size=10, text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(S.SPACE_1)
            )
            bars.append(bar)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Vencimentos por Mês", size=14, weight=ft.FontWeight.BOLD),
                ft.Row(bars, alignment=ft.MainAxisAlignment.SPACE_AROUND)
            ], spacing=S.SPACE_4),
            padding=ft.padding.all(S.SPACE_4),
            border=ft.border.all(1, C.BORDER),
            border_radius=R.RADIUS_MD
        )
    
    @staticmethod
    def create_value_chart(atas: List[Ata]) -> ft.Container:
        """Cria gráfico de valores das atas por status"""
        # Calcula valores por status
        values_by_status = {"vigente": 0, "a_vencer": 0, "vencida": 0}
        
        for ata in atas:
            values_by_status[ata.status] += ata.valor_total
        
        total_value = sum(values_by_status.values())
        
        if total_value == 0:
            return ft.Container(
                content=ft.Text("Nenhum valor cadastrado"),
                padding=ft.padding.all(S.SPACE_4)
            )
        
        # Cria barras horizontais
        bars = []
        colors = {
            "vigente": C.SUCCESS_TEXT,
            "a_vencer": C.WARNING_TEXT,
            "vencida": C.ERROR_TEXT,
        }
        
        labels = {
            "vigente": "Vigentes",
            "a_vencer": "A Vencer",
            "vencida": "Vencidas"
        }
        
        for status, value in values_by_status.items():
            if value > 0:
                percentage = (value / total_value) * 100
                bar_width = (percentage / 100) * 200  # Largura máxima de 200px
                
                # Formata valor monetário
                value_formatted = f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                
                bar = ft.Container(
                    content=ft.Row([
                        ft.Text(labels[status], width=80),
                        ft.Container(
                            width=bar_width,
                            height=20,
                            bgcolor=colors[status],
                            border_radius=R.RADIUS_XS
                        ),
                        ft.Text(f"{percentage:.1f}% ({value_formatted})", size=12)
                    ], spacing=S.SPACE_2, alignment=ft.MainAxisAlignment.START),
                    margin=ft.margin.only(bottom=S.SPACE_2)
                )
                bars.append(bar)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Valores por Status", size=14, weight=ft.FontWeight.BOLD),
                ft.Text(
                    f"Total: R$ {total_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                    size=12,
                    color=C.TEXT_SECONDARY,
                ),
                ft.Column(bars, spacing=0)
            ], spacing=S.SPACE_4),
            padding=ft.padding.all(S.SPACE_4),
            border=ft.border.all(1, C.BORDER),
            border_radius=R.RADIUS_MD
        )
    
    @staticmethod
    def create_urgency_indicator(atas_vencimento: List[Ata]) -> ft.Container:
        """Cria indicador de urgência para atas próximas do vencimento"""
        if not atas_vencimento:
            return ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.CHECK_CIRCLE, color=C.SUCCESS_TEXT, size=24),
                    ft.Text(
                        "Nenhuma ata próxima do vencimento",
                        color=C.SUCCESS_TEXT,
                    ),
                ], spacing=S.SPACE_2),
                padding=ft.padding.all(S.SPACE_4),
                border=ft.border.all(1, C.SUCCESS_TEXT),
                border_radius=R.RADIUS_MD,
                bgcolor=C.SUCCESS_BG,
            )
        
        # Classifica por urgência
        urgente = len([ata for ata in atas_vencimento if ata.dias_restantes <= 7])
        atencao = len([ata for ata in atas_vencimento if 8 <= ata.dias_restantes <= 30])
        alerta = len([ata for ata in atas_vencimento if 31 <= ata.dias_restantes <= 90])
        
        # Determina cor e ícone baseado na urgência
        if urgente > 0:
            color = C.ERROR_TEXT
            bgcolor = C.ERROR_BG
            icon = ft.icons.ERROR
            message = f"🚨 {urgente} ata(s) vencendo em 7 dias ou menos!"
        elif atencao > 0:
            color = C.WARNING_TEXT
            bgcolor = C.WARNING_BG
            icon = ft.icons.WARNING
            message = f"⚠️ {atencao} ata(s) vencendo em 30 dias ou menos!"
        else:
            color = C.PRIMARY
            bgcolor = C.BG_APP
            icon = ft.icons.INFO
            message = f"ℹ️ {alerta} ata(s) vencendo em 90 dias ou menos"
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=color, size=24),
                ft.Column([
                    ft.Text(message, weight=ft.FontWeight.BOLD, color=color),
                    ft.Text(f"Total de atas monitoradas: {len(atas_vencimento)}", size=12)
                ], spacing=S.SPACE_1)
            ], spacing=S.SPACE_2),
            padding=ft.padding.all(S.SPACE_4),
            border=ft.border.all(1, color),
            border_radius=R.RADIUS_MD,
            bgcolor=bgcolor
        )
    
    @staticmethod
    def create_summary_cards(stats: Dict[str, int], total_value: float) -> ft.Row:
        """Cria cards de resumo com estatísticas principais"""
        total_atas = sum(stats.values())
        
        cards = []
        
        # Card Total de Atas
        card_total = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Total de Atas",
                        size=12,
                        color=C.TEXT_SECONDARY,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(str(total_atas), size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "cadastradas",
                        size=10,
                        color=C.TEXT_SECONDARY,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=S.SPACE_1,
            ),
            padding=ft.padding.all(S.SPACE_4),
            border=ft.border.all(1, C.BORDER),
            border_radius=R.RADIUS_MD,
            bgcolor=C.SURFACE,
            width=160,
        )
        cards.append(card_total)
        
        # Card Valor Total
        value_formatted = f"R$ {total_value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        card_value = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Valor Total",
                        size=12,
                        color=C.TEXT_SECONDARY,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(value_formatted, size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "em atas",
                        size=10,
                        color=C.TEXT_SECONDARY,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=S.SPACE_1,
            ),
            padding=ft.padding.all(S.SPACE_4),
            border=ft.border.all(1, C.BORDER),
            border_radius=R.RADIUS_MD,
            bgcolor=C.SURFACE,
            width=160,
        )
        cards.append(card_value)
        
        # Card Vigentes
        vigentes_pct = (stats["vigente"] / total_atas * 100) if total_atas > 0 else 0
        card_vigentes = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Vigentes",
                        size=12,
                        color=C.TEXT_SECONDARY,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(
                        str(stats["vigente"]),
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=C.SUCCESS_TEXT,
                    ),
                    ft.Text(
                        f"{vigentes_pct:.1f}%",
                        size=10,
                        color=C.TEXT_SECONDARY,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=S.SPACE_1,
            ),
            padding=ft.padding.all(S.SPACE_4),
            border=ft.border.all(1, C.SUCCESS_TEXT),
            border_radius=R.RADIUS_MD,
            bgcolor=C.SUCCESS_BG,
            width=160,
        )
        cards.append(card_vigentes)
        
        # Card A Vencer
        vencer_pct = (stats["a_vencer"] / total_atas * 100) if total_atas > 0 else 0
        card_vencer = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "A Vencer",
                        size=12,
                        color=C.TEXT_SECONDARY,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(
                        str(stats["a_vencer"]),
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=C.WARNING_TEXT,
                    ),
                    ft.Text(
                        f"{vencer_pct:.1f}%",
                        size=10,
                        color=C.TEXT_SECONDARY,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=S.SPACE_1,
            ),
            padding=ft.padding.all(S.SPACE_4),
            border=ft.border.all(1, C.WARNING_TEXT),
            border_radius=R.RADIUS_MD,
            bgcolor=C.WARNING_BG,
            width=160,
        )
        cards.append(card_vencer)

        return ft.Row(cards, spacing=S.SPACE_4, alignment=ft.MainAxisAlignment.SPACE_EVENLY)

