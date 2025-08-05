#!/usr/bin/env python3
"""
Script de teste para verificar importações do projeto
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Testa todas as importações principais"""
    try:
        print("🧪 Testando importações...")
        
        # Testa modelos
        from models.ata import Ata, Item
        print("✓ Modelos OK")
        
        # Testa serviços
        from services.ata_service import AtaService
        from services.sqlite_ata_service import SQLiteAtaService
        print("✓ Serviço de Atas OK")
        print("✓ Serviço SQLite OK")
        
        from services.alert_service import AlertService
        print("✓ Serviço de Alertas OK")
        
        # Testa utilitários
        from utils.validators import Validators, Formatters, MaskUtils
        print("✓ Validadores OK")
        
        from utils.email_service import EmailService
        print("✓ Serviço de Email OK")

        from utils.chart_utils import ChartUtils
        print("✓ Utilitários de Gráficos OK")
        
        from utils.scheduler import TaskScheduler
        print("✓ Agendador OK")

        from ui.theme.colors import get_theme
        import flet as ft
        assert get_theme(ft.ThemeMode.DARK).sidebar_bg == ft.colors.GREY_800
        print("✓ Tema escuro OK")
        
        # Testa formulários
        # from forms.ata_form import AtaForm
        # print("✓ Formulários OK")
        
        print("\n✅ Todos os testes de importação passaram!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_basic_functionality():
    """Testa funcionalidades básicas"""
    try:
        print("\n🧪 Testando funcionalidades básicas...")
        
        # Testa criação de item
        from models.ata import Item
        item = Item("Teste", 1, 100.0)
        assert item.valor_total == 100.0
        print("✓ Criação de Item OK")
        
        # Testa validadores
        from utils.validators import Validators
        assert Validators.validar_numero_ata("0001/2024") == True
        assert Validators.validar_numero_ata("invalid") == False
        print("✓ Validadores OK")
        
        # Testa formatadores
        from utils.validators import Formatters
        from datetime import date
        data_formatada = Formatters.formatar_data_brasileira(date(2024, 12, 31))
        assert data_formatada == "31/12/2024"
        print("✓ Formatadores OK")
        
        # Testa serviço de atas
        from services.ata_service import AtaService
        from services.sqlite_ata_service import SQLiteAtaService
        ata_service = AtaService("test_atas.json")
        stats = ata_service.get_estatisticas()
        assert isinstance(stats, dict)
        print("✓ Serviço de Atas OK")

        sqlite_service = SQLiteAtaService(":memory:")
        stats_db = sqlite_service.get_estatisticas()
        assert isinstance(stats_db, dict)
        print("✓ Serviço SQLite OK")
        
        print("\n✅ Todos os testes de funcionalidade passaram!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de funcionalidade: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes do projeto Ata de Registro de Preços\n")
    
    success = True
    
    # Testa importações
    if not test_imports():
        success = False
    
    # Testa funcionalidades básicas
    if not test_basic_functionality():
        success = False
    
    if success:
        print("\n🎉 Todos os testes passaram com sucesso!")
        sys.exit(0)
    else:
        print("\n💥 Alguns testes falharam!")
        sys.exit(1)

