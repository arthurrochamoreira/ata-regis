# gerenciador_atas_final.py
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import datetime
import re
import copy
from collections import defaultdict
from typing import List, Dict, Any

import database
from matplotlib.figure import Figure

# ===============================================================
# 1. DATA MANAGER (BACK-END COM BANCO DE DADOS)
# ===============================================================
class DataManager:
    """Gerencia os dados da aplicação utilizando SQLite."""

    def __init__(self):
        database.init_db()

    def get_all_records(self) -> List[Dict[str, Any]]:
        return database.get_all_atas()

    def get_record(self, record_id: int) -> Dict | None:
        for record in database.get_all_atas():
            if record["id"] == record_id:
                return record
        return None

    def add_record(self, data: Dict[str, Any]) -> None:
        timestamp = datetime.datetime.now().isoformat()
        payload = copy.deepcopy(data)
        payload["createdAt"] = timestamp
        payload["updatedAt"] = timestamp
        database.insert_ata(payload)

    def update_record(self, record_id: int, data: Dict[str, Any]) -> None:
        payload = copy.deepcopy(data)
        payload["updatedAt"] = datetime.datetime.now().isoformat()
        database.update_ata(record_id, payload)

    def delete_record(self, record_id: int) -> None:
        database.delete_ata(record_id)

# ===============================================================
# 2. HELPERS DE MÁSCARA
# ===============================================================
def _aplicar_mascara(texto_digitado: str, mascara: str) -> str:
    digitos = re.sub(r'\D', '', texto_digitado)
    saida, i = [], 0
    for ch in mascara:
        if ch.isdigit() or ch.isalpha():
            if i < len(digitos):
                saida.append(digitos[i])
                i += 1
            else:
                saida.append(ch)
        else:
            saida.append(ch)
    return ''.join(saida)

def _handler_mascara(app: "AtaApp", mascara: str):
    placeholders = {c for c in mascara if c.isdigit() or c.isalpha()}
    def _on_change(e: ft.ControlEvent):
        novo_valor = _aplicar_mascara(e.control.value, mascara)
        e.control.value = novo_valor
        prox = next((idx for idx, ch in enumerate(novo_valor) if ch in placeholders), len(novo_valor))
        if e.control.page:
            e.control.selection_start = e.control.selection_end = prox
            e.control.page.update()
    return _on_change

# ===============================================================
# 3. CLASSE PRINCIPAL DA APLICAÇÃO FLET
# ===============================================================
class AtaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Gerenciador de Atas de Registro de Preços"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1366
        self.page.window_height = 900
        self.page.window_min_width = 1200
        self.page.window_min_height = 800

        self.data_manager = DataManager()
        self.current_edit_ata_id = None
        self.atas = []
        
        self.colors = {
            'primary_blue': '#0078d4', 'secondary_blue': '#deecf9',
            'status_active': '#107c10', 'status_warning': '#ff8c00',
            'status_expired': '#d13438', 'gray_50': '#faf9f8',
            'gray_100': '#f3f2f1', 'gray_200': '#edebe9',
            'gray_700': '#605e5c', 'gray_800': '#323130', 'white': '#ffffff'
        }

        # --- Referências de UI ---
        self.kpi_cards = {}
        self.status_chart = MatplotlibChart(expand=True)
        self.expiry_chart = MatplotlibChart(expand=True)
        self.data_table = ft.DataTable(columns=[], rows=[]) 
        self.vigentes_column = None
        self.proximas_column = None
        self.vencidas_column = None
        self.modal = self._create_modal()
        self.page.dialog = self.modal

        self._setup_ui()
        self.load_and_refresh_all()

    def _setup_ui(self):
        header = self._create_header()
        dashboard_view = self._create_dashboard_view()
        kanban_view = self._create_kanban_view()
        
        tabs = ft.Tabs(
            selected_index=0, animation_duration=300,
            tabs=[
                ft.Tab(text="Dashboard", content=dashboard_view),
                ft.Tab(text="Painel Kanban", content=kanban_view),
            ],
            expand=True,
        )
        self.page.add(ft.Column([header, tabs], expand=True, spacing=0))

    def _create_header(self) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ASSIGNMENT, color=self.colors['white'], size=24),
                        bgcolor=self.colors['primary_blue'], border_radius=8, padding=12, width=48, height=48
                    ),
                    ft.Column([
                        ft.Text("Atas de Registro de Preços", size=24, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        ft.Text("Gerencie as atas em um painel centralizado", size=14, color=self.colors['gray_700'])
                    ], spacing=2)
                ], spacing=16),
                ft.ElevatedButton(
                    "Nova Ata", icon=ft.Icons.ADD, on_click=self.open_modal,
                    bgcolor=self.colors['primary_blue'], color=self.colors['white']
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=self.colors['white'], padding=ft.padding.symmetric(horizontal=32, vertical=16),
            border=ft.border.only(bottom=ft.BorderSide(1, self.colors['gray_200']))
        )

    def _create_dashboard_view(self) -> ft.Container:
        kpi_labels = ["Total de Atas", "Vigentes", "A Vencer", "Vencidas"]
        kpi_row_content = []
        for label in kpi_labels:
            value_text = ft.Text("0", size=24, weight="bold", color=self.colors['gray_800'])
            label_text = ft.Text(label, size=14, color=self.colors['gray_700'])
            card = ft.Container(
                content=ft.Column([value_text, label_text], spacing=2),
                padding=20, border_radius=8, bgcolor=self.colors['white'],
                border=ft.border.all(1, self.colors['gray_200']), expand=True
            )
            self.kpi_cards[label] = value_text
            kpi_row_content.append(card)
        
        self.data_table.columns = [
            ft.DataColumn(ft.Text("Status", weight="bold")),
            ft.DataColumn(ft.Text("Nº da Ata", weight="bold")),
            ft.DataColumn(ft.Text("Objeto", weight="bold")),
            ft.DataColumn(ft.Text("Vigência", weight="bold")),
        ]

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(controls=kpi_row_content, spacing=20),
                    ft.Row(
                        [
                            ft.Container(self.status_chart, padding=10, border_radius=8, bgcolor=self.colors['white'], border=ft.border.all(1, self.colors['gray_200']), expand=1),
                            ft.Container(self.expiry_chart, padding=10, border_radius=8, bgcolor=self.colors['white'], border=ft.border.all(1, self.colors['gray_200']), expand=2),
                        ], spacing=20, height=320
                    ),
                    ft.Container(
                        ft.Column([
                            ft.Text("Todas as Atas", size=18, weight="bold", color=self.colors['gray_800']),
                            ft.Container(content=self.data_table, border_radius=8, border=ft.border.all(1, self.colors['gray_200']))
                        ]),
                        padding=20, border_radius=8, bgcolor=self.colors['white']
                    )
                ], 
                scroll=ft.ScrollMode.ADAPTIVE, spacing=20
            ),
            padding=32, bgcolor=self.colors['gray_100'], expand=True
        )

    def _create_kanban_view(self) -> ft.Container:
        self.vigentes_column = self._create_kanban_column("Vigentes", self.colors['status_active'], 0)
        self.proximas_column = self._create_kanban_column("Próximas ao Vencimento", self.colors['status_warning'], 0)
        self.vencidas_column = self._create_kanban_column("Vencidas", self.colors['status_expired'], 0)
        
        return ft.Container(
            content=ft.Row(
                controls=[self.vigentes_column, self.proximas_column, self.vencidas_column],
                spacing=24, expand=True, alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START
            ),
            padding=32, bgcolor=self.colors['gray_50'], expand=True,
        )

    def _create_kanban_column(self, title: str, color: str, count: int) -> ft.Container:
        header = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(width=12, height=12, bgcolor=color, border_radius=6),
                    ft.Text(title, size=16, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                    ft.Container(
                        content=ft.Text(str(count), size=12, weight=ft.FontWeight.W_600, color=self.colors['gray_700']),
                        bgcolor=self.colors['gray_200'], padding=ft.padding.symmetric(horizontal=8, vertical=4), border_radius=12
                    )
                ], spacing=8),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(16), border=ft.border.only(bottom=ft.BorderSide(1, self.colors['gray_200']))
        )
        
        cards_column = ft.Column([], spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)

        return ft.Container(
            content=ft.Column([header, ft.Container(content=cards_column, padding=16, expand=True)], spacing=0),
            bgcolor=self.colors['white'], border_radius=12,
            border=ft.border.all(1, self.colors['gray_200']), expand=True,
        )

    def _create_kanban_card(self, ata: Dict[str, Any]) -> ft.Container:
        today = datetime.date.today()
        vigencia_date = datetime.datetime.strptime(ata['dataVigencia'], "%Y-%m-%d").date()
        assinatura_date = datetime.datetime.strptime(ata['dataAssinatura'], "%Y-%m-%d").date()
        is_expired = vigencia_date < today
        total_duration = max(1, (vigencia_date - assinatura_date).days)
        elapsed_duration = max(0, (today - assinatura_date).days)
        progress = min(1.0, (elapsed_duration / total_duration)) if not is_expired else 1.0
        
        status_text, status_color = self._get_status_info(ata)

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(ata['objeto'], size=16, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        ft.Text(f"Ata: {ata['numeroAta']} | SEI: {ata.get('documentoSei', 'N/A')}", size=12, color=self.colors['gray_700'])
                    ], expand=True),
                    ft.Container(
                        content=ft.Text(status_text, size=10, weight=ft.FontWeight.W_600, color=self.colors['white']),
                        bgcolor=status_color, padding=ft.padding.symmetric(horizontal=8, vertical=4), border_radius=12
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Column([
                    ft.Row([
                        ft.Text("Progresso", size=12, color=self.colors['gray_700']),
                        ft.Text(f"Venc.: {vigencia_date.strftime('%d/%m/%Y')}", size=12, color=self.colors['gray_700'])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.ProgressBar(value=progress, bgcolor=self.colors['gray_200'], color=self.colors['primary_blue'])
                ], spacing=4),
                ft.Text(f"Fornecedor: {ata.get('fornecedor', 'N/A')}", size=14, color=self.colors['gray_700']),
                ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_color=self.colors['primary_blue'], on_click=lambda e, ata_id=ata['id']: self.edit_ata(ata_id), tooltip="Editar"),
                    ft.IconButton(ft.Icons.DELETE, icon_color=self.colors['status_expired'], on_click=lambda e, ata_id=ata['id']: self.delete_ata(ata_id), tooltip="Excluir")
                ], alignment=ft.MainAxisAlignment.END, spacing=0)
            ], spacing=12),
            bgcolor=self.colors['white'], border=ft.border.all(1, self.colors['gray_200']), border_radius=8, padding=16
        )

    def load_and_refresh_all(self):
        self.atas = self.data_manager.get_all_records()
        self._refresh_dashboard_view()
        self._refresh_kanban_view()
        if self.page: self.page.update()

    def _refresh_dashboard_view(self):
        self._update_kpis()
        self._update_charts()
        self._update_data_table()

    def _refresh_kanban_view(self):
        self._update_kanban_columns()

    def _update_kpis(self):
        counts = self._get_status_counts()
        self.kpi_cards["Total de Atas"].value = str(len(self.atas))
        self.kpi_cards["Vigentes"].value = str(counts['Vigente'])
        self.kpi_cards["A Vencer"].value = str(counts['A Vencer'])
        self.kpi_cards["Vencidas"].value = str(counts['Vencida'])

    def _update_charts(self):
        counts = self._get_status_counts()
        labels = ['Vigente', 'A Vencer', 'Vencida']
        sizes = [counts.get(l, 0) for l in labels]
        colors = [self.colors['status_active'], self.colors['status_warning'], self.colors['status_expired']]
        
        fig1 = Figure(figsize=(4, 3), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.set_title("Distribuição por Status")
        self.status_chart.figure = fig1

        monthly_counts = defaultdict(int)
        for ata in self.atas:
            status, _ = self._get_status_info(ata)
            if status in ['Vigente', 'A Vencer']:
                month = int(ata['dataVigencia'][5:7])
                monthly_counts[month] += 1
        
        month_labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        month_values = [monthly_counts.get(i + 1, 0) for i in range(12)]
        
        fig2 = Figure(figsize=(5, 3), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.bar(month_labels, month_values, color=self.colors['primary_blue'])
        ax2.set_ylabel('Nº de Atas')
        ax2.set_title('Vencimentos Futuros por Mês')
        fig2.tight_layout(pad=0.5)
        self.expiry_chart.figure = fig2
    
    def _update_data_table(self):
        self.data_table.rows.clear()
        for ata in sorted(self.atas, key=lambda a: a['dataVigencia']):
            status, color = self._get_status_info(ata)
            self.data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(status, color=color, weight="bold")),
                    ft.DataCell(ft.Text(ata['numeroAta'])),
                    ft.DataCell(ft.Text(ata['objeto'], max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)),
                    ft.DataCell(ft.Text(datetime.datetime.strptime(ata['dataVigencia'], '%Y-%m-%d').strftime('%d/%m/%Y'))),
                ])
            )

    def _update_kanban_columns(self):
        vigentes, proximas, vencidas = [], [], []
        for ata in self.atas:
            status, _ = self._get_status_info(ata)
            if status == 'Vencida': vencidas.append(ata)
            elif status == 'A Vencer': proximas.append(ata)
            else: vigentes.append(ata)

        self._update_single_kanban_column(self.vigentes_column, vigentes)
        self._update_single_kanban_column(self.proximas_column, proximas)
        self._update_single_kanban_column(self.vencidas_column, vencidas)

    def _update_single_kanban_column(self, column: ft.Container, atas: List[Dict]):
        if column and column.content:
            header_row = column.content.controls[0].content
            count_container = header_row.controls[0].controls[2]
            count_container.content.value = str(len(atas))
            
            cards_column = column.content.controls[1].content
            cards_column.controls = [self._create_kanban_card(ata) for ata in atas]

    def _get_status_info(self, ata: Dict[str, Any]) -> (str, str):
        today = datetime.date.today()
        ninety_days = today + datetime.timedelta(days=90)
        try:
            vigencia_date = datetime.datetime.strptime(ata['dataVigencia'], "%Y-%m-%d").date()
            if vigencia_date < today: return "Vencida", self.colors['status_expired']
            if vigencia_date <= ninety_days: return "A Vencer", self.colors['status_warning']
            return "Vigente", self.colors['status_active']
        except (ValueError, KeyError, TypeError):
            return "Inválida", self.colors['gray_700']

    def _get_status_counts(self) -> Dict[str, int]:
        counts = defaultdict(int)
        for ata in self.atas:
            status, _ = self._get_status_info(ata)
            counts[status] += 1
        return counts

    def _create_modal(self) -> ft.AlertDialog:
        self.numero_ata_field = ft.TextField(label="Número da Ata", value="NNNN/NNNN", on_change=_handler_mascara(self, "NNNN/NNNN"))
        self.documento_sei_field = ft.TextField(label="Documento SEI", hint_text="Ex: 12345.67890/2024-11")
        self.objeto_field = ft.TextField(label="Objeto", hint_text="Descrição do objeto da ata")
        self.data_assinatura_field = ft.TextField(label="Data de Assinatura", value="DD/MM/AAAA", on_change=_handler_mascara(self, "DD/MM/AAAA"))
        self.data_vigencia_field = ft.TextField(label="Data de Vigência", value="DD/MM/AAAA", on_change=_handler_mascara(self, "DD/MM/AAAA"))
        self.fornecedor_field = ft.TextField(label="Nome do Fornecedor", hint_text="Nome da empresa fornecedora")
        
        self.telefones_list = ft.Column([], spacing=8, scroll=ft.ScrollMode.AUTO)
        self.emails_list = ft.Column([], spacing=8, scroll=ft.ScrollMode.AUTO)
        self.items_list = ft.Column([], spacing=12, scroll=ft.ScrollMode.AUTO)

        modal_content = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text("Formulário da Ata", size=24, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        ft.IconButton(ft.Icons.CLOSE, on_click=self.close_modal, icon_color=self.colors['gray_700'])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.all(24), border=ft.border.only(bottom=ft.BorderSide(1, self.colors['gray_200']))
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Informações Básicas", size=18, weight=ft.FontWeight.W_600),
                        ft.Row([self.numero_ata_field, self.documento_sei_field], spacing=16),
                        self.objeto_field,
                        ft.Row([self.data_assinatura_field, self.data_vigencia_field], spacing=16),
                        ft.Divider(height=24),
                        ft.Text("Dados do Fornecedor", size=18, weight=ft.FontWeight.W_600),
                        self.fornecedor_field,
                        ft.Row([
                            ft.Column([
                                ft.Text("Telefones"),
                                ft.Container(content=self.telefones_list, border=ft.border.all(1, self.colors['gray_200']), border_radius=5, height=85, padding=5),
                                ft.OutlinedButton("Adicionar", icon=ft.Icons.ADD, on_click=self.add_telefone_field)
                            ], expand=True),
                            ft.Column([
                                ft.Text("E-mails"),
                                ft.Container(content=self.emails_list, border=ft.border.all(1, self.colors['gray_200']), border_radius=5, height=85, padding=5),
                                ft.OutlinedButton("Adicionar", icon=ft.Icons.ADD, on_click=self.add_email_field)
                            ], expand=True)
                        ], spacing=24),
                        ft.Divider(height=24),
                        ft.Row([ft.Text("Itens da Ata", size=18, weight=ft.FontWeight.W_600), ft.OutlinedButton("Adicionar Item", icon=ft.Icons.ADD, on_click=self.add_item_field)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(content=self.items_list, expand=True, border=ft.border.all(1, self.colors['gray_200']), border_radius=5, padding=5)
                    ], spacing=16, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.all(24), expand=True
                ),
                ft.Container(
                    content=ft.Row([
                        ft.OutlinedButton("Cancelar", on_click=self.close_modal),
                        ft.ElevatedButton("Salvar", icon=ft.Icons.SAVE, on_click=self.save_ata, bgcolor=self.colors['primary_blue'], color=self.colors['white'])
                    ], alignment=ft.MainAxisAlignment.END, spacing=12),
                    padding=ft.padding.all(24), border=ft.border.only(top=ft.BorderSide(1, self.colors['gray_200']))
                )
            ], spacing=0),
            bgcolor=self.colors['white'], border_radius=12, width=800, height=750
        )
        return ft.AlertDialog(modal=True, content=modal_content, content_padding=0)

    # ===============================================================
    # FUNÇÃO CORRIGIDA
    # ===============================================================
    def _clear_modal_fields(self):
        """Limpa e reseta todos os campos do modal para o estado inicial."""
        # Reseta os valores dos campos de texto
        self.numero_ata_field.value = "NNNN/NNNN"
        self.documento_sei_field.value = ""
        self.objeto_field.value = ""
        self.fornecedor_field.value = ""
        self.data_assinatura_field.value = "DD/MM/AAAA"
        self.data_vigencia_field.value = "DD/MM/AAAA"

        # Limpa qualquer texto de erro
        for field in [self.numero_ata_field, self.documento_sei_field, self.objeto_field, 
                      self.fornecedor_field, self.data_assinatura_field, self.data_vigencia_field]:
            field.error_text = None
        
        # Limpa as listas dinâmicas
        self.telefones_list.controls.clear()
        self.emails_list.controls.clear()
        self.items_list.controls.clear()

    def add_field_with_remove(self, parent_list: ft.Column, hint_text: str):
        field_row = ft.Row([
            ft.TextField(hint_text=hint_text, expand=True),
            ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE, on_click=lambda e: self.remove_field(parent_list, e.control.data), icon_color=self.colors['gray_700'])
        ])
        field_row.controls[1].data = field_row
        parent_list.controls.append(field_row)
        self.page.update()

    def add_telefone_field(self, e=None): self.add_field_with_remove(self.telefones_list, "(XX) XXXX-XXXX")
    def add_email_field(self, e=None): self.add_field_with_remove(self.emails_list, "contato@empresa.com")
    def add_item_field(self, e=None):
        item_container = ft.Container(
            content=ft.Column([
                ft.Row([ft.Text(f"Item {len(self.items_list.controls) + 1}", weight="bold"), ft.IconButton(ft.Icons.DELETE, on_click=lambda e: self.remove_field(self.items_list, e.control.data), icon_color=self.colors['status_expired'])]),
                ft.TextField(label="Descrição"), ft.Row([ft.TextField(label="Qtd", expand=1), ft.TextField(label="Valor Unit. (R$)", expand=2)])
            ], spacing=8),
            bgcolor=self.colors['gray_50'], border=ft.border.all(1, self.colors['gray_200']), border_radius=8, padding=16
        )
        item_container.content.controls[0].controls[1].data = item_container
        self.items_list.controls.append(item_container)
        self.page.update()

    def remove_field(self, parent_list: ft.Column, field_to_remove):
        parent_list.controls.remove(field_to_remove)
        if parent_list == self.items_list:
            for i, item_container in enumerate(parent_list.controls):
                item_container.content.controls[0].controls[0].value = f"Item {i + 1}"
        self.page.update()

    def open_modal(self, e=None):
        self.current_edit_ata_id = None
        self._clear_modal_fields()
        self.modal.content.content.controls[0].content.controls[0].value = "Criar Nova Ata"
        self.modal.open = True
        self.page.update()
        
    def close_modal(self, e=None):
        self.modal.open = False
        self.page.update()

    # ===============================================================
    # FUNÇÃO CORRIGIDA
    # ===============================================================
    def save_ata(self, e=None):
        """Valida os dados do formulário e salva uma nova ata ou atualiza uma existente."""
        # --- 1. Reset e Validação ---
        is_valid = True
        all_fields = [
            self.numero_ata_field,
            self.objeto_field,
            self.fornecedor_field,
            self.data_assinatura_field,
            self.data_vigencia_field,
        ]
        for field in all_fields:
            field.error_text = None

        if 'N' in self.numero_ata_field.value:
            self.numero_ata_field.error_text = "Preencha o número completo."
            is_valid = False
        if not self.objeto_field.value.strip():
            self.objeto_field.error_text = "O objeto é obrigatório."
            is_valid = False

        if not self.fornecedor_field.value.strip():
            self.fornecedor_field.error_text = "O fornecedor é obrigatório."
            is_valid = False
        
        data_assinatura_obj, data_vigencia_obj = None, None
        try:
            data_assinatura_obj = datetime.datetime.strptime(self.data_assinatura_field.value, "%d/%m/%Y")
        except ValueError:
            self.data_assinatura_field.error_text = "Data de assinatura inválida."
            is_valid = False
        try:
            data_vigencia_obj = datetime.datetime.strptime(self.data_vigencia_field.value, "%d/%m/%Y")
        except ValueError:
            self.data_vigencia_field.error_text = "Data de vigência inválida."
            is_valid = False

        if data_assinatura_obj and data_vigencia_obj and data_vigencia_obj < data_assinatura_obj:
            self.data_vigencia_field.error_text = "Vigência não pode ser anterior à assinatura."
            is_valid = False

        if not is_valid:
            self.page.update()
            return

        # --- 2. Coleta de Dados ---
        items_data = []
        for item_container in self.items_list.controls:
            desc_field = item_container.content.controls[1]
            qtd_field = item_container.content.controls[2].controls[0]
            valor_field = item_container.content.controls[2].controls[1]
            try:
                quantidade = int(qtd_field.value) if qtd_field.value else 0
            except (ValueError, TypeError):
                quantidade = 0
            try:
                valor_str = valor_field.value.replace(',', '.') if valor_field.value else '0'
                valor = float(valor_str)
            except (ValueError, TypeError):
                valor = 0.0
            if desc_field.value or quantidade or valor:
                items_data.append({'descricao': desc_field.value, 'quantidade': quantidade, 'valor': valor})

        ata_data = {
            'numeroAta': self.numero_ata_field.value.strip(),
            'documentoSei': self.documento_sei_field.value.strip(),
            'objeto': self.objeto_field.value.strip(),
            'dataAssinatura': data_assinatura_obj.strftime("%Y-%m-%d"),
            'dataVigencia': data_vigencia_obj.strftime("%Y-%m-%d"),
            'fornecedor': self.fornecedor_field.value.strip(),
            'telefonesFornecedor': [row.controls[0].value.strip() for row in self.telefones_list.controls if row.controls[0].value.strip()],
            'emailsFornecedor': [row.controls[0].value.strip() for row in self.emails_list.controls if row.controls[0].value.strip()],
            'items': items_data
        }
        
        # --- 3. Salvar Dados ---
        if self.current_edit_ata_id is not None:
            self.data_manager.update_record(self.current_edit_ata_id, ata_data)
        else:
            self.data_manager.add_record(ata_data)

        self.load_and_refresh_all()
        self.close_modal()
        self.show_snackbar("Ata salva com sucesso!", self.colors['status_active'])


    def edit_ata(self, ata_id: int):
        ata = self.data_manager.get_record(ata_id)
        if ata:
            self.current_edit_ata_id = ata_id
            self._clear_modal_fields()
            
            self.numero_ata_field.value = ata.get('numeroAta', '')
            self.documento_sei_field.value = ata.get('documentoSei', '')
            self.objeto_field.value = ata.get('objeto', '')
            self.fornecedor_field.value = ata.get('fornecedor', '')
            
            try:
                self.data_assinatura_field.value = datetime.datetime.strptime(ata['dataAssinatura'], '%Y-%m-%d').strftime('%d/%m/%Y')
            except: pass
            try:
                self.data_vigencia_field.value = datetime.datetime.strptime(ata['dataVigencia'], '%Y-%m-%d').strftime('%d/%m/%Y')
            except: pass
            
            for tel in ata.get('telefonesFornecedor', []):
                self.add_telefone_field()
                self.telefones_list.controls[-1].controls[0].value = tel
            
            for email in ata.get('emailsFornecedor', []):
                self.add_email_field()
                self.emails_list.controls[-1].controls[0].value = email
            
            for item in ata.get('items', []):
                self.add_item_field()
                self.items_list.controls[-1].content.controls[1].value = item.get('descricao', '')
                self.items_list.controls[-1].content.controls[2].controls[0].value = str(item.get('quantidade', ''))
                self.items_list.controls[-1].content.controls[2].controls[1].value = str(item.get('valor', '')).replace('.',',')
            
            for field in [self.numero_ata_field, self.data_assinatura_field, self.data_vigencia_field]:
                if field.on_change:
                    field.on_change(ft.ControlEvent(target=field.uid, name="change", data=field.value, control=field, page=self.page))
            
            self.modal.content.content.controls[0].content.controls[0].value = f"Editar Ata {ata.get('numeroAta', '')}"
            self.modal.open = True
            self.page.update()

    def delete_ata(self, ata_id: int):
        def confirm_delete(e):
            self.data_manager.delete_record(ata_id)
            self.load_and_refresh_all()
            self.show_snackbar("Ata excluída!", self.colors['status_active'])
            confirm_dialog.open = False
            self.page.dialog = self.modal # Restaura o diálogo principal
            self.page.update()

        def cancel_delete(e):
            confirm_dialog.open = False
            self.page.dialog = self.modal # Restaura o diálogo principal
            self.page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Confirmar Exclusão"), content=ft.Text("Tem certeza?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_delete), 
                ft.TextButton("Excluir", on_click=confirm_delete, style=ft.ButtonStyle(color=self.colors['status_expired']))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()

    def show_snackbar(self, message: str, color: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(message, color=self.colors['white']), bgcolor=color, duration=3000)
        self.page.snack_bar.open = True
        self.page.update()

# ===============================================================
# 4. PONTO DE ENTRADA DA APLICAÇÃO
# ===============================================================
def main(page: ft.Page):
    AtaApp(page)

if __name__ == "__main__":
    ft.app(target=main)