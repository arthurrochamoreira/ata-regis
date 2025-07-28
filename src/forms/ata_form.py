import flet as ft
from datetime import date, datetime
from typing import List, Dict, Any, Optional, Callable

try:
    from ..ui.tokens import (
        SPACE_2,
        SPACE_3,
        SPACE_4,
        SPACE_5,
        PRIMARY,
    )
except Exception:  # pragma: no cover
    from ui.tokens import SPACE_2, SPACE_3, SPACE_4, SPACE_5, PRIMARY
try:
    from ..models.ata import Ata, Item
    from ..utils.validators import Validators, Formatters, MaskUtils
except ImportError:  # Execução direta sem pacote
    from models.ata import Ata, Item
    from utils.validators import Validators, Formatters, MaskUtils

class AtaForm:
    """Formulário para criação e edição de atas"""
    
    def __init__(self, page: ft.Page, on_save: Callable[[Dict[str, Any]], None], 
                 on_cancel: Callable[[], None], ata: Optional[Ata] = None):
        self.page = page
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.ata = ata
        self.is_edit_mode = ata is not None
        
        # Campos do formulário
        self.numero_ata_field = None
        self.documento_sei_field = None
        self.data_vigencia_field = None
        self.objeto_field = None
        self.fornecedor_field = None
        self.telefones_container = None
        self.emails_container = None
        self.itens_container = None
        
        # Listas dinâmicas
        self.telefones = []
        self.emails = []
        self.itens = []
        
        self.build_form()
    
    def build_form(self):
        """Constrói o formulário"""
        # Título
        titulo = "Editar Ata" if self.is_edit_mode else "Nova Ata"
        
        # Campos básicos
        self.numero_ata_field = ft.TextField(
            label="Número da Ata",
            hint_text="0000/0000",
            on_change=self.on_numero_ata_change,
            width=200,
            border_radius=8,  # inputs radius=8 (Style Guide)
        )
        
        self.documento_sei_field = ft.TextField(
            label="Documento SEI",
            hint_text="00000.000000/0000-00",
            on_change=self.on_documento_sei_change,
            width=300,
            border_radius=8,
        )
        
        self.data_vigencia_field = ft.TextField(
            label="Data de Vigência",
            hint_text="DD/MM/AAAA",
            width=200,
            border_radius=8,
        )
        
        self.objeto_field = ft.TextField(
            label="Objeto",
            hint_text="Descrição do objeto da ata",
            width=400,
            multiline=True,
            max_lines=3,
            border_radius=8,
        )
        
        self.fornecedor_field = ft.TextField(
            label="Fornecedor",
            hint_text="Nome da empresa fornecedora",
            width=400,
            border_radius=8,
        )
        
        # Containers para listas dinâmicas
        self.telefones_container = ft.Column(spacing=SPACE_2)
        self.emails_container = ft.Column(spacing=SPACE_2)
        self.itens_container = ft.Column(spacing=SPACE_2)
        
        # Preenche campos se estiver editando
        if self.is_edit_mode:
            self.populate_fields()
        else:
            # Adiciona campos vazios para nova ata
            self.add_telefone()
            self.add_email()
            self.add_item()
        
        # Seções do formulário
        dados_gerais = ft.Container(
            content=ft.Column(
                [
                    ft.Text("📋 Dados Gerais", size=18, weight=ft.FontWeight.SEMI_BOLD),
                    ft.Row([self.numero_ata_field, self.documento_sei_field], spacing=SPACE_5),
                    ft.Row([self.data_vigencia_field], spacing=SPACE_5),
                    self.objeto_field,
                    self.fornecedor_field,
                ],
                spacing=SPACE_5,
            ),
            padding=ft.padding.all(SPACE_5),  # padding=24 (Style Guide)
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=12,  # cards radius=12 (Style Guide)
            margin=ft.margin.only(bottom=SPACE_5)
        )
        
        telefones_section = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("📞 Telefones", size=18, weight=ft.FontWeight.SEMI_BOLD),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                tooltip="Adicionar telefone",
                                on_click=lambda e: self.add_telefone(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.telefones_container,
                ],
                spacing=SPACE_2,
            ),
            padding=ft.padding.all(SPACE_5),
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=12,
            margin=ft.margin.only(bottom=SPACE_5),
        )
        
        emails_section = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("📧 E-mails", size=18, weight=ft.FontWeight.SEMI_BOLD),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                tooltip="Adicionar e-mail",
                                on_click=lambda e: self.add_email(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.emails_container,
                ],
                spacing=SPACE_2,
            ),
            padding=ft.padding.all(SPACE_5),
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=12,
            margin=ft.margin.only(bottom=SPACE_5),
        )
        
        itens_section = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("🧾 Itens", size=18, weight=ft.FontWeight.SEMI_BOLD),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                tooltip="Adicionar item",
                                on_click=lambda e: self.add_item(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.itens_container,
                ],
                spacing=SPACE_2,
            ),
            padding=ft.padding.all(SPACE_5),
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=12,
            margin=ft.margin.only(bottom=SPACE_5),
        )
        
        # Botões
        botoes = ft.Row([
            ft.ElevatedButton(
                "Cancelar",
                on_click=lambda e: self.on_cancel(),
                color=ft.colors.ON_SURFACE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            ),
            ft.ElevatedButton(
                "Salvar",
                on_click=self.save_ata,
                bgcolor=PRIMARY,
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            )
        ], alignment=ft.MainAxisAlignment.END, spacing=SPACE_5)
        
        # Layout principal
        content = ft.Column([
            ft.Text(titulo, size=24, weight=ft.FontWeight.SEMI_BOLD),
            dados_gerais,
            telefones_section,
            emails_section,
            itens_section,
            botoes
        ], spacing=0, scroll=ft.ScrollMode.AUTO)
        
        # Dialog
        self.dialog = ft.AlertDialog(
            title=ft.Text(titulo),
            content=ft.Container(
                content=content,
                width=800,
                height=600
            ),
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
    
    def populate_fields(self):
        """Preenche os campos com dados da ata existente"""
        if not self.ata:
@@ -212,119 +246,124 @@ class AtaForm:
        self.numero_ata_field.value = self.ata.numero_ata
        self.documento_sei_field.value = self.ata.documento_sei
        self.data_vigencia_field.value = self.ata.data_vigencia.strftime("%d/%m/%Y")
        self.objeto_field.value = self.ata.objeto
        self.fornecedor_field.value = self.ata.fornecedor
        
        # Telefones
        for telefone in self.ata.telefones_fornecedor:
            self.add_telefone(telefone)
        
        # E-mails
        for email in self.ata.emails_fornecedor:
            self.add_email(email)
        
        # Itens
        for item in self.ata.itens:
            self.add_item(item)
    
    def add_telefone(self, valor: str = ""):
        """Adiciona campo de telefone"""
        telefone_field = ft.TextField(
            label=f"Telefone {len(self.telefones) + 1}",
            hint_text="(XX) XXXXX-XXXX",
            value=valor,
            on_change=self.on_telefone_change,
            width=200,
            border_radius=8,
        )
        
        remove_btn = ft.IconButton(
            icon=ft.icons.DELETE,
            tooltip="Remover telefone"
        )

        row = ft.Row([telefone_field, remove_btn], spacing=SPACE_2)
        remove_btn.on_click = lambda e, field=telefone_field, r=row: self.remove_telefone(field, r)
        self.telefones.append((telefone_field, row))
        self.telefones_container.controls.append(row)
        self.page.update()
    
    def remove_telefone(self, field, row):
        """Remove campo de telefone"""
        self.telefones = [(f, r) for f, r in self.telefones if f != field]
        if row in self.telefones_container.controls:
            self.telefones_container.controls.remove(row)
        self.page.update()
    
    def add_email(self, valor: str = ""):
        """Adiciona campo de e-mail"""
        email_field = ft.TextField(
            label=f"E-mail {len(self.emails) + 1}",
            hint_text="email@exemplo.com",
            value=valor,
            width=300,
            border_radius=8,
        )
        
        remove_btn = ft.IconButton(
            icon=ft.icons.DELETE,
            tooltip="Remover e-mail"
        )

        row = ft.Row([email_field, remove_btn], spacing=SPACE_2)
        remove_btn.on_click = lambda e, field=email_field, r=row: self.remove_email(field, r)
        self.emails.append((email_field, row))
        self.emails_container.controls.append(row)
        self.page.update()
    
    def remove_email(self, field, row):
        """Remove campo de e-mail"""
        self.emails = [(f, r) for f, r in self.emails if f != field]
        if row in self.emails_container.controls:
            self.emails_container.controls.remove(row)
        self.page.update()
    
    def add_item(self, item: Optional[Item] = None):
        """Adiciona campos de item"""
        descricao_field = ft.TextField(
            label="Descrição",
            hint_text="Descrição do item",
            value=item.descricao if item else "",
            width=300,
            border_radius=8,
        )
        
        quantidade_field = ft.TextField(
            label="Quantidade",
            hint_text="0",
            value=str(item.quantidade) if item else "",
            width=100,
            border_radius=8,
        )
        
        valor_field = ft.TextField(
            label="Valor Unitário",
            hint_text="0,00",
            value=f"{item.valor:.2f}".replace(".", ",") if item else "",
            width=150,
            border_radius=8,
        )
        
        remove_btn = ft.IconButton(
            icon=ft.icons.DELETE,
            tooltip="Remover item",
            on_click=lambda e: self.remove_item(descricao_field, row)
        )
        
        row = ft.Row([
            descricao_field,
            quantidade_field,
            valor_field,
            remove_btn
        ], spacing=SPACE_2)
        
        self.itens.append((descricao_field, quantidade_field, valor_field, row))
        self.itens_container.controls.append(row)
        self.page.update()
    
    def remove_item(self, descricao_field, row):
        """Remove campos de item"""
        self.itens = [(d, q, v, r) for d, q, v, r in self.itens if d != descricao_field]
        if row in self.itens_container.controls:
            self.itens_container.controls.remove(row)
        self.page.update()