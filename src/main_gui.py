import flet as ft
import sys
import os

# Adiciona o diretório src ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.sqlite_ata_service import SQLiteAtaService
from services.alert_service import AlertService
from utils.email_service import EmailService
from utils.scheduler import TaskScheduler
from forms.ata_form import AtaForm
from ui.main_view import (
    build_header,
    build_filters,
    build_search,
    build_grouped_cards,
    build_atas_vencimento,
    build_stats_panel as ui_build_stats_panel,
)
from ui.navigation_menu import LeftNavigationMenu
from ui import build_ata_detail_view
from ui.theme.spacing import SPACE_2, SPACE_4, SPACE_5
from ui.responsive import get_breakpoint

class AtaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.ata_service = SQLiteAtaService()
        self.email_service = EmailService()
        self.alert_service = AlertService(self.email_service)
        self.scheduler = TaskScheduler(self.ata_service, self.alert_service)
        self.filtro_atual = "todos"
        self.texto_busca = ""
        self.current_tab = 0
        self.breakpoint = get_breakpoint(page.width)
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
        # Remove outer page padding to ensure consistent gutter handled by body container
        self.page.padding = 0
        self.page.bgcolor = "#F3F4F6"
        self.page.fonts = {"Inter": "https://fonts.gstatic.com/s/inter/v7/Inter-Regular.ttf"}
        self.page.theme = ft.Theme(font_family="Inter")
        self.page.on_resize = self.on_page_resize
    
    def build_ui(self):
        """Constrói a interface do usuário usando navegação lateral"""
        self.page.appbar = build_header(
            nova_ata_cb=self.nova_ata_click,
            verificar_alertas_cb=self.verificar_alertas_manual,
            relatorio_semanal_cb=lambda e: self.gerar_relatorio_manual("semanal"),
            relatorio_mensal_cb=lambda e: self.gerar_relatorio_manual("mensal"),
            testar_email_cb=self.testar_email,
            status_cb=self.mostrar_status_sistema,
        )

        self.navigation_menu = LeftNavigationMenu(self)
        self.body_container = ft.Container(
            padding=ft.padding.only(top=SPACE_4, bottom=SPACE_4),
            expand=True,
        )
        self.update_body()

        self.menu_container = ft.Container(
            content=self.navigation_menu,
            width=200,
            bgcolor=ft.colors.WHITE,
            padding=ft.padding.only(
                left=SPACE_5,
                right=SPACE_5,
                top=SPACE_5,
                bottom=SPACE_5,
            ),
            shadow=ft.BoxShadow(blur_radius=1, spread_radius=0),
        )

        layout = ft.Row(
            [self.menu_container, self.body_container],
            expand=True,
        )

        self.page.add(layout)
        self.update_responsive_layout(self.page.width)
        self.page.update()

    def update_responsive_layout(self, width: int):
        """Atualiza visibilidade e dimensões da barra lateral conforme ``width``."""
        self.navigation_menu.update_layout(width)

        if width < 768:
            self.menu_container.visible = False
        elif width < 1024:
            self.menu_container.visible = True
            self.menu_container.width = 80
            self.menu_container.padding = ft.padding.all(SPACE_2)
        else:
            self.menu_container.visible = True
            self.menu_container.width = 200
            self.menu_container.padding = ft.padding.all(SPACE_5)

        self.page.update()
    
    def build_stats_panel(self):
        """Retorna o painel de estatísticas"""
        return ui_build_stats_panel(self.ata_service)
    
    
    def build_atas_vencimento(self):
        """Retorna atas próximas do vencimento"""
        return build_atas_vencimento(
            self.ata_service.get_atas_vencimento_proximo(),
            self.visualizar_ata,
            self.enviar_alerta,
        )

    def build_dashboard_view(self):
        self.stats_container = ui_build_stats_panel(self.ata_service)
        return ft.Column([self.stats_container], spacing=0, expand=True)

    def build_atas_view(self):
        filtros = build_filters(self.filtro_atual, self.filtrar_atas)
        search_container, self.search_field = build_search(
            self.buscar_atas, self.texto_busca
        )
        filtros.margin = ft.margin.only(bottom=0)
        search_container.margin = ft.margin.only(bottom=0)
        filtros.col = {"xs": 12, "md": 4, "lg": 4}
        search_container.col = {"xs": 12, "md": 8, "lg": 8}
        filtros_search_row = ft.Container(
            content=ft.ResponsiveRow(
                [filtros, search_container],
                columns=12,
                spacing=SPACE_4,
                run_spacing=SPACE_4,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            margin=ft.margin.only(bottom=0),
        )
        self.grouped_cards = build_grouped_cards(
            self.get_atas_filtradas(),
            self.visualizar_ata,
            self.editar_ata,
            self.excluir_ata,
            filtro=self.filtro_atual,
        )
        return ft.Column([filtros_search_row, self.grouped_cards], spacing=0, expand=True)

    def build_vencimentos_view(self):
        self.atas_vencimento_container = build_atas_vencimento(
            self.ata_service.get_atas_vencimento_proximo(),
            self.visualizar_ata,
            self.enviar_alerta,
        )
        return ft.Column([self.atas_vencimento_container], spacing=0, expand=True)

    def update_body(self):
        if self.current_tab == 0:
            content = self.build_dashboard_view()
        elif self.current_tab == 1:
            content = self.build_atas_view()
        else:
            content = self.build_vencimentos_view()
        self.body_container.content = content
        self.page.update()

    def navigate_to(self, index: int):
        self.current_tab = index
        self.update_body()

    def on_page_resize(self, e):
        self.update_responsive_layout(self.page.width)
        new_bp = get_breakpoint(self.page.width)
        if new_bp != self.breakpoint:
            self.breakpoint = new_bp
            self.refresh_ui()
    
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
        # Atualiza apenas a tabela mantendo o texto digitado
        new_table = build_grouped_cards(
            self.get_atas_filtradas(),
            self.visualizar_ata,
            self.editar_ata,
            self.excluir_ata,
            filtro=self.filtro_atual,
        )
        self.grouped_cards.content = new_table.content
        self.search_field.value = self.texto_busca
        self.page.update()
    
    def refresh_ui(self):
        """Atualiza a interface"""
        self.update_body()

    
    def nova_ata_click(self, e):
        """Abre o formulário para nova ata"""
        AtaForm(
            page=self.page,
            on_save=self.salvar_nova_ata,
            on_cancel=self.fechar_formulario
        )
    
    def visualizar_ata(self, ata):
        """Visualiza uma ata usando o layout moderno"""
        detail_view = build_ata_detail_view(
            ata,
            on_back=lambda e: self.close_dialog(),
            on_edit=lambda e: self.editar_ata(ata),
        )

        self.page.dialog = ft.AlertDialog(
            content=detail_view,
            actions=[],
            modal=True,
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

