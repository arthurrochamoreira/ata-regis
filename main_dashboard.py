import datetime
from typing import List, Dict, Any

import flet as ft
import database

# -----------------------
# Helpers
# -----------------------

def compute_status(record: Dict[str, Any]) -> Dict[str, Any]:
    """Return status information for a record."""
    today = datetime.date.today()
    try:
        vigencia_date = datetime.datetime.strptime(record['dataVigencia'], '%Y-%m-%d').date()
    except Exception:
        return {'text': 'Inv\u00e1lida', 'color': ft.colors.GREY, 'days': 9999}
    days = (vigencia_date - today).days
    if days < 0:
        return {'text': 'Vencida', 'color': ft.colors.RED, 'days': days}
    if days <= 90:
        return {'text': 'A Vencer', 'color': ft.colors.YELLOW, 'days': days}
    return {'text': 'Vigente', 'color': ft.colors.GREEN, 'days': days}


def format_date(value: str) -> str:
    try:
        return datetime.datetime.strptime(value, '%Y-%m-%d').strftime('%d/%m/%Y')
    except Exception:
        return value or ''


# -----------------------
# App Class
# -----------------------

class DashboardApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Dashboard de Atas'
        self.records: List[Dict[str, Any]] = []
        self.filter_status = 'all'
        self.search_text = ''
        self.sort_column = 4
        self.sort_asc = True
        database.init_db()
        self.load_records(refresh=True)
        self.build_ui()
        self.refresh_dashboard()

    # --------- Data ---------
    def load_records(self, refresh: bool = False):
        self.records = database.get_all_atas()
        if refresh:
            self.refresh_dashboard()

    # --------- UI Builders ---------
    def build_ui(self):
        self.new_btn = ft.ElevatedButton('Nova Ata', icon=ft.icons.ADD, on_click=self.open_new_modal)
        header = ft.Row([
            ft.Text('Dashboard de Atas', size=24, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            self.new_btn,
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        self.search_field = ft.TextField(placeholder='Pesquisar...', on_change=self.on_search, width=250)

        # KPI area
        self.kpi_container = ft.Row(spacing=20)
        self.update_kpis()

        # Charts
        self.status_chart = ft.PieChart(height=200, sections=[])
        self.expiry_chart = ft.BarChart(height=200, bar_groups=[])
        charts_row = ft.Row([
            ft.Container(self.status_chart, expand=2),
            ft.Container(self.expiry_chart, expand=3)
        ], spacing=20)

        # Featured
        self.featured_list = ft.Column(spacing=8)
        self.featured_container = ft.Container(
            content=ft.Column([
                ft.Text('Atas em Destaque', weight=ft.FontWeight.BOLD),
                self.featured_list
            ], spacing=10),
            visible=False,
            bgcolor=ft.colors.WHITE,
            padding=10,
            border_radius=8
        )

        # Table area
        self.table = ft.DataTable(columns=[
            ft.DataColumn(ft.Text('Status'), on_sort=self.on_sort),
            ft.DataColumn(ft.Text('N\u00ba Ata'), on_sort=self.on_sort),
            ft.DataColumn(ft.Text('Objeto'), on_sort=self.on_sort),
            ft.DataColumn(ft.Text('Fornecedor'), on_sort=self.on_sort),
            ft.DataColumn(ft.Text('Vig\u00eancia'), on_sort=self.on_sort),
            ft.DataColumn(ft.Text('A\u00e7\u00f5es')),
        ], rows=[])
        self.update_table()

        self.page.add(
            ft.Column([
                header,
                self.kpi_container,
                charts_row,
                self.featured_container,
                ft.Row([self.search_field], alignment=ft.MainAxisAlignment.END),
                ft.Divider(),
                self.table,
            ], expand=True)
        )

    def update_kpis(self):
        counts = {'Vigente': 0, 'A Vencer': 0, 'Vencida': 0}
        for r in self.records:
            status = compute_status(r)['text']
            if status in counts:
                counts[status] += 1
        total = len(self.records)
        self.kpi_container.controls = [
            self.kpi_card('Total de Atas', total, ft.colors.BLUE, 'all'),
            self.kpi_card('Vigentes', counts['Vigente'], ft.colors.GREEN, 'Vigente'),
            self.kpi_card('A Vencer (90d)', counts['A Vencer'], ft.colors.YELLOW, 'A Vencer'),
            self.kpi_card('Vencidas', counts['Vencida'], ft.colors.RED, 'Vencida'),
        ]
        self.page.update()

    def kpi_card(self, label: str, value: int, color: str, status: str) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Text(label, size=14, color=ft.colors.GREY_600),
                ft.Text(str(value), size=24, weight=ft.FontWeight.BOLD, color=color),
            ], spacing=4),
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            padding=10,
            width=150,
            on_click=lambda e, s=status: self.set_filter(s),
        )

    def update_charts(self):
        status_counts = {'Vigente': 0, 'A Vencer': 0, 'Vencida': 0}
        for r in self.records:
            st = compute_status(r)['text']
            if st in status_counts:
                status_counts[st] += 1
        self.status_chart.sections = [
            ft.PieChartSection(value=status_counts.get('Vigente', 0), color=ft.colors.GREEN, title=str(status_counts.get('Vigente', 0))),
            ft.PieChartSection(value=status_counts.get('A Vencer', 0), color=ft.colors.YELLOW, title=str(status_counts.get('A Vencer', 0))),
            ft.PieChartSection(value=status_counts.get('Vencida', 0), color=ft.colors.RED, title=str(status_counts.get('Vencida', 0)))
        ]

        month_counts = [0]*12
        for r in self.records:
            st = compute_status(r)
            if st['text'] in ('Vigente', 'A Vencer'):
                try:
                    m = datetime.datetime.strptime(r['dataVigencia'], '%Y-%m-%d').month - 1
                    month_counts[m] += 1
                except Exception:
                    pass

        groups = []
        for i, val in enumerate(month_counts):
            groups.append(ft.BarChartGroup(x=i, bar_rods=[ft.BarChartRod(to_y=val, width=20, color=ft.colors.BLUE)]))
        self.expiry_chart.bar_groups = groups
        self.page.update()

    def update_featured(self):
        records = sorted(self.records, key=lambda r: compute_status(r)['days'])
        near = [r for r in records if compute_status(r)['text'] in ('A Vencer', 'Vigente')][:3]
        self.featured_list.controls.clear()
        if not near:
            self.featured_container.visible = False
            return
        self.featured_container.visible = True
        for r in near:
            status = compute_status(r)
            card = ft.Container(
                content=ft.Column([
                    ft.Text(r['objeto'], weight=ft.FontWeight.BOLD),
                    ft.Text(f"Ata {r['numeroAta']} - {r['fornecedor']}", size=12),
                    ft.Text(f"{status['days']} dias", color=status['color'], size=12)
                ], spacing=2),
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=8,
                padding=8,
            )
            self.featured_list.controls.append(card)
        self.page.update()

    def update_table(self):
        rows = []
        records = [r for r in self.records if (self.filter_status == 'all' or compute_status(r)['text'] == self.filter_status)]
        if self.search_text:
            term = self.search_text.lower()
            records = [r for r in records if term in f"{r.get('objeto','')} {r.get('numeroAta','')} {r.get('fornecedor','')}".lower()]

        def sort_key(rec):
            if self.sort_column == 0:
                return compute_status(rec)['days']
            if self.sort_column == 1:
                return rec.get('numeroAta','')
            if self.sort_column == 2:
                return rec.get('objeto','')
            if self.sort_column == 3:
                return rec.get('fornecedor','')
            if self.sort_column == 4:
                return rec.get('dataVigencia','')
            return 0

        records.sort(key=sort_key, reverse=not self.sort_asc)
        for r in records:
            status = compute_status(r)
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(status['text'])),
                ft.DataCell(ft.Text(r.get('numeroAta', ''))),
                ft.DataCell(ft.Text(r.get('objeto', ''))),
                ft.DataCell(ft.Text(r.get('fornecedor', ''))),
                ft.DataCell(ft.Text(format_date(r.get('dataVigencia', '')))),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.icons.REMOVE_RED_EYE, on_click=lambda e, rec=r: self.view_record(rec)),
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, rec=r: self.edit_record(rec)),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, rec=r: self.delete_record(rec)),
                ])),
            ])
            rows.append(row)
        self.table.rows = rows
        self.page.update()

    def refresh_dashboard(self):
        self.update_kpis()
        self.update_charts()
        self.update_featured()
        self.update_table()

    def set_filter(self, status: str):
        self.filter_status = status
        self.refresh_dashboard()

    def on_search(self, e):
        self.search_text = e.control.value
        self.refresh_dashboard()

    def on_sort(self, e: ft.DataColumnSortEvent):
        self.sort_column = e.column_index
        self.sort_asc = e.ascending
        self.refresh_dashboard()

    # --------- Modal forms ---------
    def open_new_modal(self, e=None):
        self.open_modal(None)

    def edit_record(self, record):
        self.open_modal(record)

    def open_modal(self, record: Dict[str, Any] | None):
        is_edit = record is not None
        title = 'Editar Ata' if is_edit else 'Nova Ata'
        self.modal_numero = ft.TextField(label='N\u00ba da Ata', value=record.get('numeroAta', '') if record else '')
        self.modal_documento = ft.TextField(label='Documento SEI', value=record.get('documentoSei', '') if record else '')
        self.modal_objeto = ft.TextField(label='Objeto', value=record.get('objeto', '') if record else '')
        self.modal_assinatura = ft.TextField(label='Data de Assinatura', value=record.get('dataAssinatura', '') if record else '')
        self.modal_vigencia = ft.TextField(label='Data de Vig\u00eancia', value=record.get('dataVigencia', '') if record else '')
        self.modal_fornecedor = ft.TextField(label='Fornecedor', value=record.get('fornecedor', '') if record else '')

        def save_record(e):
            data = {
                'numeroAta': self.modal_numero.value,
                'documentoSei': self.modal_documento.value,
                'objeto': self.modal_objeto.value,
                'dataAssinatura': self.modal_assinatura.value,
                'dataVigencia': self.modal_vigencia.value,
                'fornecedor': self.modal_fornecedor.value,
                'telefonesFornecedor': [],
                'emailsFornecedor': [],
                'items': [],
                'updatedAt': datetime.datetime.now().isoformat(),
            }
            if is_edit:
                data['updatedAt'] = datetime.datetime.now().isoformat()
                database.update_ata(record['id'], data)
            else:
                data['createdAt'] = datetime.datetime.now().isoformat()
                database.insert_ata(data)
            dlg.open = False
            self.load_records(refresh=True)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Column([
                self.modal_numero,
                self.modal_documento,
                self.modal_objeto,
                self.modal_assinatura,
                self.modal_vigencia,
                self.modal_fornecedor,
            ], width=400, height=400, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton('Cancelar', on_click=lambda e: setattr(dlg, 'open', False) or self.page.update()),
                ft.ElevatedButton('Salvar', on_click=save_record),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def view_record(self, record):
        status = compute_status(record)
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text('Detalhes da Ata'),
            content=ft.Column([
                ft.Text(f"Status: {status['text']}", color=status['color']),
                ft.Text(f"N\u00ba: {record.get('numeroAta')}", selectable=True),
                ft.Text(f"Objeto: {record.get('objeto')}", selectable=True),
                ft.Text(f"Fornecedor: {record.get('fornecedor')}", selectable=True),
                ft.Text(f"Vig\u00eancia: {format_date(record.get('dataVigencia'))}"),
            ], width=400),
            actions=[ft.TextButton('Fechar', on_click=lambda e: setattr(dlg, 'open', False) or self.page.update())],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def delete_record(self, record):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text('Excluir Ata?'),
            content=ft.Text('Esta ac\u00e7\u00e3o n\u00e3o pode ser desfeita.'),
            actions=[
                ft.TextButton('Cancelar', on_click=lambda e: setattr(dlg, 'open', False) or self.page.update()),
                ft.TextButton('Excluir', on_click=lambda e: self._confirm_delete(record, dlg), style=ft.ButtonStyle(color=ft.colors.RED)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def _confirm_delete(self, record, dlg):
        database.delete_ata(record['id'])
        dlg.open = False
        self.load_records(refresh=True)


# -----------------------
# Entry Point
# -----------------------

def main(page: ft.Page):
    DashboardApp(page)


if __name__ == '__main__':
    ft.app(target=main)
