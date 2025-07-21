import flet as ft
import datetime
from typing import List, Dict, Any
import sys
import os

# Adiciona o diretório src ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ata_service import AtaService
from services.alert_service import AlertService
from utils.email_service import EmailService
from utils.validators import Formatters
from utils.chart_utils import ChartUtils
from utils.scheduler import TaskScheduler
from forms.ata_form import AtaForm

class AtaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.ata_service = AtaService()
        self.email_service = EmailService()
        self.alert_service = AlertService(self.email_service)
        self.scheduler = TaskScheduler(self.ata_service, self.alert_service)
        self.filtro_atual = "todos"
        self.texto_busca = ""
        self.setup_page()
        self.build_ui()
        
        # Inicia o agendador de tarefas
        self.scheduler.start()
    
    def setup_page(self):
        """Configurações da página"""
        self.page.title = "Ata de Registro de Preços 0016/2024"
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 16
        self.apply_apple_theme()

    def apply_apple_theme(self):
        """Aplica um tema minimalista inspirado no visual do macOS/iOS"""
        self.page.theme = ft.Theme(
            font_family="Helvetica",
            color_scheme=ft.ColorScheme(
                primary=ft.colors.BLUE,
                on_primary=ft.colors.WHITE,
                background=ft.colors.WHITE,
                surface=ft.colors.WHITE,
                on_surface=ft.colors.BLACK,
                outline=ft.colors.GREY_300,
            ),
        )
        self.page.update()

    def apple_button(self, text: str, on_click, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE):
        """Cria um botão no estilo iOS/macOS"""
        return ft.ElevatedButton(
            text,
            on_click=on_click,
            bgcolor=bgcolor,
            color=color,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
            ),
        )
    
    def build_ui(self):
        """Constrói a interface do usuário"""
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Text("📝 Ata de Registro de Preços", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.PopupMenuButton(
                        icon=ft.icons.SETTINGS,
                        tooltip="Ferramentas",
                        items=[
                            ft.PopupMenuItem(
                                text="🔍 Verificar Alertas",
                                on_click=self.verificar_alertas_manual
                            ),
                            ft.PopupMenuItem(
                                text="📊 Relatório Semanal",
                                on_click=lambda e: self.gerar_relatorio_manual("semanal")
                            ),
                            ft.PopupMenuItem(
                                text="📈 Relatório Mensal",
                                on_click=lambda e: self.gerar_relatorio_manual("mensal")
                            ),
                            ft.PopupMenuItem(
                                text="📧 Testar Email",
                                on_click=self.testar_email
                            ),
                            ft.PopupMenuItem(
                                text="ℹ️ Status Sistema",
                                on_click=self.mostrar_status_sistema
                            )
                        ]
                    ),
                    self.apple_button(
                        "➕ Nova Ata",
                        on_click=self.nova_ata_click
                    )
                ], spacing=8)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(16),
            margin=ft.margin.only(bottom=16)
        )
        
        # Painel de estatísticas
        self.stats_container = self.build_stats_panel()
        
        # Filtros
        filtros = ft.Container(
            content=ft.Row([
                self.apple_button(
                    "✅ Vigentes",
                    on_click=lambda e: self.filtrar_atas("vigente"),
                    bgcolor=ft.colors.GREEN if self.filtro_atual == "vigente" else ft.colors.SURFACE_VARIANT,
                    color=ft.colors.BLACK if self.filtro_atual != "vigente" else ft.colors.WHITE,
                ),
                self.apple_button(
                    "⚠️ A Vencer",
                    on_click=lambda e: self.filtrar_atas("a_vencer"),
                    bgcolor=ft.colors.ORANGE if self.filtro_atual == "a_vencer" else ft.colors.SURFACE_VARIANT,
                    color=ft.colors.BLACK if self.filtro_atual != "a_vencer" else ft.colors.WHITE,
                ),
                self.apple_button(
                    "❌ Vencidas",
                    on_click=lambda e: self.filtrar_atas("vencida"),
                    bgcolor=ft.colors.RED if self.filtro_atual == "vencida" else ft.colors.SURFACE_VARIANT,
                    color=ft.colors.BLACK if self.filtro_atual != "vencida" else ft.colors.WHITE,
                ),
                self.apple_button(
                    "📋 Todas",
                    on_click=lambda e: self.filtrar_atas("todos"),
                    bgcolor=ft.colors.BLUE if self.filtro_atual == "todos" else ft.colors.SURFACE_VARIANT,
                    color=ft.colors.BLACK if self.filtro_atual != "todos" else ft.colors.WHITE,
                )
            ], spacing=10),
            padding=ft.padding.all(16),
            margin=ft.margin.only(bottom=16)
        )
        
        # Campo de busca
        self.search_field = ft.TextField(
            label="Buscar atas...",
            prefix_icon=ft.icons.SEARCH,
            on_change=self.buscar_atas,
            width=400
        )
        
        search_container = ft.Container(
            content=self.search_field,
            padding=ft.padding.all(16),
            margin=ft.margin.only(bottom=16)
        )
        
        # Tabela de atas
        self.data_table = self.build_data_table()
        
        # Seção de atas próximas do vencimento
        self.atas_vencimento_container = self.build_atas_vencimento()
        
        # Layout principal
        main_content = ft.Column([
            header,
            self.stats_container,
            filtros,
            search_container,
            self.data_table,
            self.atas_vencimento_container
        ], spacing=0, expand=True)
        
        self.page.add(main_content)
        self.page.update()
    
    def build_stats_panel(self):
        """Constrói o painel de estatísticas com gráficos melhorados"""
        stats = self.ata_service.get_estatisticas()
        atas = self.ata_service.listar_todas()
        atas_vencimento = self.ata_service.get_atas_vencimento_proximo()
        
        total_value = sum(ata.valor_total for ata in atas)
        
        # Cards de resumo
        summary_cards = ChartUtils.create_summary_cards(stats, total_value)
        
        # Gráfico de pizza e legenda
        pie_chart = ChartUtils.create_status_pie_chart(stats)
        legend = ChartUtils.create_status_legend(stats)
        
        # Indicador de urgência
        urgency_indicator = ChartUtils.create_urgency_indicator(atas_vencimento)
        
        # Gráfico de valores por status
        value_chart = ChartUtils.create_value_chart(atas)
        
        # Gráfico mensal
        monthly_chart = ChartUtils.create_monthly_chart(atas)
        
        # Layout principal do painel
        main_chart_row = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("📊 Situação das Atas", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([pie_chart, legend], spacing=32, alignment=ft.MainAxisAlignment.START)
                ], spacing=16),
                padding=ft.padding.all(16),
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=8,
                expand=True
            ),
            ft.Container(
                content=value_chart,
                width=300
            )
        ], spacing=16)
        
        return ft.Container(
            content=ft.Column([
                summary_cards,
                urgency_indicator,
                main_chart_row,
                monthly_chart
            ], spacing=16),
            margin=ft.margin.only(bottom=24)
        )
    
    def build_data_table(self):
        """Constrói a tabela de dados das atas"""
        rows = []
        atas_filtradas = self.get_atas_filtradas()
        
        for ata in atas_filtradas:
            status_icon = "✅" if ata.status == "vigente" else "⚠️" if ata.status == "a_vencer" else "❌"
            
            # Formatação da data
            data_formatada = Formatters.formatar_data_brasileira(ata.data_vigencia)
            
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(ata.numero_ata)),
                    ft.DataCell(ft.Text(data_formatada)),
                    ft.DataCell(ft.Text(ata.objeto)),
                    ft.DataCell(ft.Text(ata.fornecedor)),
                    ft.DataCell(ft.Text(f"{status_icon} {ata.status.replace('_', ' ').title()}")),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.VISIBILITY,
                                tooltip="Visualizar",
                                on_click=lambda e, ata=ata: self.visualizar_ata(ata)
                            ),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda e, ata=ata: self.editar_ata(ata)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip="Excluir",
                                on_click=lambda e, ata=ata: self.excluir_ata(ata)
                            )
                        ], spacing=0)
                    )
                ]
            )
            rows.append(row)
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Número")),
                ft.DataColumn(ft.Text("Vigência")),
                ft.DataColumn(ft.Text("Objeto")),
                ft.DataColumn(ft.Text("Fornecedor")),
                ft.DataColumn(ft.Text("Situação")),
                ft.DataColumn(ft.Text("Ações"))
            ],
            rows=rows,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=8
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📋 Lista de Atas", size=18, weight=ft.FontWeight.BOLD),
                table
            ], spacing=16),
            padding=ft.padding.all(16),
            margin=ft.margin.only(bottom=24)
        )
    
    def build_atas_vencimento(self):
        """Constrói a seção de atas próximas do vencimento"""
        atas_vencimento = self.ata_service.get_atas_vencimento_proximo()
        
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
                        ft.Text(f"Faltam {ata.dias_restantes} dias", 
                               color=ft.colors.RED if ata.dias_restantes <= 30 else ft.colors.ORANGE)
                    ], spacing=4),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.VISIBILITY,
                            tooltip="Visualizar",
                            on_click=lambda e, ata=ata: self.visualizar_ata(ata)
                        ),
                        ft.IconButton(
                            icon=ft.icons.EMAIL,
                            tooltip="Enviar Alerta",
                            on_click=lambda e, ata=ata: self.enviar_alerta(ata)
                        )
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(12),
                margin=ft.margin.only(bottom=8),
                border=ft.border.all(1, ft.colors.ORANGE),
                border_radius=8,
                bgcolor=ft.colors.ORANGE_50
            )
            items.append(item)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("🔔 Atas Próximas do Vencimento", size=18, weight=ft.FontWeight.BOLD),
                ft.Column(items, spacing=0)
            ], spacing=16),
            padding=ft.padding.all(16),
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=8
        )
    
    def get_atas_filtradas(self):
        """Retorna as atas filtradas baseado no filtro atual e busca"""
        atas = self.ata_service.listar_todas()
        
        # Aplica filtro por status
        if self.filtro_atual != "todos":
            atas = [ata for ata in atas if ata.status == self.filtro_atual]
        
        # Aplica busca por texto
        if self.texto_busca:
            atas = self.ata_service.buscar_por_texto(self.texto_busca)
            # Reaplica filtro de status se necessário
            if self.filtro_atual != "todos":
                atas = [ata for ata in atas if ata.status == self.filtro_atual]
        
        return atas
    
    def filtrar_atas(self, filtro: str):
        """Filtra as atas por status"""
        self.filtro_atual = filtro
        self.refresh_ui()
    
    def buscar_atas(self, e):
        """Busca atas por texto"""
        self.texto_busca = e.control.value.strip()
        self.refresh_ui()
    
    def refresh_ui(self):
        """Atualiza a interface"""
        self.page.controls.clear()
        self.build_ui()
    
    def nova_ata_click(self, e):
        """Abre o formulário para nova ata"""
        AtaForm(
            page=self.page,
            on_save=self.salvar_nova_ata,
            on_cancel=self.fechar_formulario
        )
    
    def visualizar_ata(self, ata):
        """Visualiza uma ata"""
        content = f"""
Número: {ata.numero_ata}
SEI: {ata.documento_sei}
Vigência: {Formatters.formatar_data_brasileira(ata.data_vigencia)}
Objeto: {ata.objeto}
Fornecedor: {ata.fornecedor}
Telefones: {', '.join(ata.telefones_fornecedor)}
E-mails: {', '.join(ata.emails_fornecedor)}

Valor Total: {Formatters.formatar_valor_monetario(ata.valor_total)}

Itens:
"""
        for i, item in enumerate(ata.itens, 1):
            content += f"{i}. {item.descricao}: {item.quantidade} x {Formatters.formatar_valor_monetario(item.valor)} = {Formatters.formatar_valor_monetario(item.valor_total)}\n"
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(f"Ata {ata.numero_ata}"),
            content=ft.Text(content),
            actions=[ft.TextButton("Fechar", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()
    
    def editar_ata(self, ata):
        """Edita uma ata"""
        AtaForm(
            page=self.page,
            on_save=lambda data: self.salvar_edicao_ata(ata.numero_ata, data),
            on_cancel=self.fechar_formulario,
            ata=ata
        )
    
    def excluir_ata(self, ata):
        """Exclui uma ata"""
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Excluir Ata"),
            content=ft.Text(f"Deseja realmente excluir a ata {ata.numero_ata}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.TextButton("Excluir", on_click=lambda e: self.confirmar_exclusao(ata.numero_ata))
            ]
        )
        self.page.dialog.open = True
        self.page.update()
    
    def confirmar_exclusao(self, numero_ata):
        """Confirma a exclusão de uma ata"""
        if self.ata_service.excluir_ata(numero_ata):
            self.close_dialog()
            self.refresh_ui()
            self.show_success_message("Ata excluída com sucesso!")
        else:
            self.show_error_message("Erro ao excluir ata.")
    
    def enviar_alerta(self, ata):
        """Envia alerta por email (simulado com print)"""
        if self.email_service.enviar_alerta_vencimento(ata):
            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Alerta Enviado"),
                content=ft.Text("Alerta de vencimento enviado com sucesso!\n(Verifique o console para detalhes)"),
                actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
            )
            self.page.dialog.open = True
            self.page.update()
        else:
            self.show_error_message("Erro ao enviar alerta.")
    
    def close_dialog(self):
        """Fecha o diálogo atual"""
        self.page.dialog.open = False
        self.page.update()

    def salvar_nova_ata(self, ata_data):
        """Salva uma nova ata"""
        try:
            self.ata_service.criar_ata(ata_data)
            self.refresh_ui()
            self.show_success_message("Ata criada com sucesso!")
        except Exception as e:
            self.show_error_message(f"Erro ao criar ata: {str(e)}")
    
    def salvar_edicao_ata(self, numero_ata, ata_data):
        """Salva a edição de uma ata"""
        try:
            self.ata_service.editar_ata(numero_ata, ata_data)
            self.refresh_ui()
            self.show_success_message("Ata atualizada com sucesso!")
        except Exception as e:
            self.show_error_message(f"Erro ao atualizar ata: {str(e)}")
    
    def fechar_formulario(self):
        """Fecha o formulário atual"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
    
    def show_success_message(self, message):
        """Mostra mensagem de sucesso"""
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Sucesso"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()
    
    def show_error_message(self, message):
        """Mostra mensagem de erro"""
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()


    
    def verificar_alertas_manual(self, e):
        """Executa verificação manual de alertas"""
        resultado = self.scheduler.executar_verificacao_manual()
        
        message = f"""Verificação de alertas concluída:

• Alertas enviados: {resultado['alertas_enviados']}
• Atas alertadas: {len(resultado['atas_alertadas'])}

"""
        
        if resultado['atas_alertadas']:
            message += "Atas alertadas:\n"
            for ata_info in resultado['atas_alertadas']:
                message += f"- {ata_info['numero_ata']} ({ata_info['tipo_alerta']})\n"
        
        if resultado['erros']:
            message += f"\nErros encontrados: {len(resultado['erros'])}\n"
            for erro in resultado['erros']:
                message += f"- {erro}\n"
        
        message += "\nVerifique o console para detalhes completos."
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Verificação de Alertas"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()
    
    def gerar_relatorio_manual(self, tipo: str):
        """Gera relatório manual"""
        if self.scheduler.gerar_relatorio_manual(tipo):
            message = f"Relatório {tipo} gerado com sucesso!\nVerifique o console para detalhes."
        else:
            message = f"Erro ao gerar relatório {tipo}."
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(f"Relatório {tipo.title()}"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()
    
    def testar_email(self, e):
        """Testa a configuração de email"""
        if self.email_service.testar_configuracao():
            message = "Configuração de email testada com sucesso!\nVerifique o console para detalhes."
        else:
            message = "Erro ao testar configuração de email."
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Teste de Email"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()
    
    def mostrar_status_sistema(self, e):
        """Mostra status do sistema"""
        status = self.scheduler.get_status()
        historico = self.alert_service.get_historico_alertas(7)  # Últimos 7 dias
        
        message = f"""Status do Sistema:

🔄 Agendador: {"Ativo" if status['running'] else "Inativo"}
🧵 Thread: {"Ativa" if status['thread_alive'] else "Inativa"}
📧 Alertas (7 dias): {len(historico)}
🕐 Última verificação: {status['ultima_verificacao']}

📊 Estatísticas:
• Total de atas: {len(self.ata_service.listar_todas())}
• Atas próximas vencimento: {len(self.ata_service.get_atas_vencimento_proximo())}

O sistema está monitorando automaticamente as atas e enviará alertas conforme necessário.
"""
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Status do Sistema"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()
    
    def __del__(self):
        """Destrutor - para o agendador ao fechar a aplicação"""
        if hasattr(self, 'scheduler'):
            self.scheduler.stop()


def main(page: ft.Page):
    app = AtaApp(page)


if __name__ == "__main__":
    ft.app(target=main)

