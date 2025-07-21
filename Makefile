.PHONY: build-up clean install run test help dev backup restore reinstall info update deps-report check-structure clean-temp

# =========================
# Configurações Gerais
# =========================
REQ=requirements.txt
VENV=.venv
SRC_DIR=src
BACKUP_DIR=backups
DATA_FILE=atas.json

# Detecta SO
OS := $(shell (uname 2>NUL) || echo Windows_NT)

ifeq ($(OS),Windows_NT)
	PYTHON=python
	PYTHON_VENV=$(VENV)\Scripts\python.exe
	PIP=$(VENV)\Scripts\pip.exe
	CHECK_REQ=$(PYTHON_VENV) scripts\check_requirements.py
	DEVNULL=NUL
else
	PYTHON=python3
	PYTHON_VENV=$(VENV)/bin/python3
	PIP=$(VENV)/bin/pip
	CHECK_REQ=$(PYTHON_VENV) scripts/check_requirements.py
	DEVNULL=/dev/null
endif

# =========================
# Ajuda
# =========================
help:
	@echo "Sistema de Gerenciamento - Ata de Registro de Preços"
	@echo ""
	@echo "Comandos disponíveis:"
	@echo "  build-up      - Configura ambiente e executa aplicação"
	@echo "  install       - Instala dependências"
	@echo "  run           - Executa a aplicação"
	@echo "  dev           - Executa em modo desenvolvimento"
	@echo "  test          - Executa testes básicos"
	@echo "  clean         - Remove ambiente virtual"
	@echo "  backup        - Faz backup dos dados"
	@echo "  restore       - Lista backups disponíveis"
	@echo "  reinstall     - Limpa e reinstala tudo"
	@echo "  info          - Mostra informações do sistema"
	@echo "  update        - Atualiza dependências"
	@echo "  deps-report   - Gera relatório de dependências"

# =========================
# Build completo
# =========================
build-up: install run

# =========================
# Instalação
# =========================
install:
	@echo "[1/3] Verificando se o Python está instalado..."
	@$(PYTHON) --version >$(DEVNULL) 2>&1 || (echo "Python não encontrado. Instale manualmente." && exit 1)
	@echo "[2/3] Criando ambiente virtual..."
	@$(PYTHON) -m venv $(VENV)
	@$(PIP) install --upgrade pip
	@echo "[3/3] Instalando dependências..."
	@$(PIP) install -r $(REQ)
	@$(CHECK_REQ)
	@echo "✅ Ambiente configurado com sucesso!"

# =========================
# Execução
# =========================
run:
	@echo "Executando aplicação..."
ifeq ($(OS),Windows_NT)
	@$(PYTHON_VENV) $(SRC_DIR)\main_gui.py
else
	@$(PYTHON_VENV) $(SRC_DIR)/main_gui.py
endif


dev:
	@echo "Executando em modo desenvolvimento (com logs detalhados)..."
	@cd $(SRC_DIR) && PYTHONPATH=. $(PYTHON_VENV) -u main_gui.py

test:
	@echo "Executando testes básicos..."
	@$(PYTHON_VENV) test_imports.py

# =========================
# Backup e restauração
# =========================
backup:
	@echo "Criando backup..."
	@mkdir -p $(BACKUP_DIR)
	@if [ -f "$(DATA_FILE)" ]; then \
		cp $(DATA_FILE) $(BACKUP_DIR)/$(DATA_FILE).backup.$$(date +%Y%m%d_%H%M%S); \
		echo "Backup de dados criado."; \
	else \
		echo "Arquivo $(DATA_FILE) não encontrado."; \
	fi
	@tar -czf $(BACKUP_DIR)/src_backup_`date +%Y%m%d_%H%M%S`.tar.gz $(SRC_DIR)

restore:
	@echo "Backups disponíveis:"
	@ls -la $(BACKUP_DIR)/*.backup.* 2>/dev/null || echo "Nenhum backup encontrado"

# =========================
# Limpeza
# =========================
clean-temp:
	@echo "Limpando arquivos temporários..."
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

clean: clean-temp
	@echo "Removendo ambiente virtual..."
	@rm -rf $(VENV)
	@echo "Ambiente limpo."

reinstall: clean install
	@echo "Reinstalação concluída."

# =========================
# Utilitários
# =========================
info:
	@echo "Informações do sistema:"
	@echo "Python: $$($(PYTHON) --version 2>&1)"
	@echo "Pip: $$($(PIP) --version 2>&1)"
	@echo "Sistema: $$(uname -s)"
	@echo "Arquitetura: $$(uname -m)"
	@echo "Diretório atual: $$(pwd)"
	@echo "Ambiente virtual: $(VENV)"
	@if [ -d "$(VENV)" ]; then \
		echo "Status: Criado"; \
		$(PIP) list | wc -l | xargs echo "Pacotes instalados:"; \
	else \
		echo "Status: Não criado"; \
	fi

update: install
	@echo "Atualizando dependências..."
	@$(PIP) install --upgrade pip
	@$(PIP) install --upgrade -r $(REQ)

deps-report: install
	@echo "Gerando relatório de dependências..."
	@$(PIP) list > deps_report.txt
	@$(PIP) freeze > requirements_freeze.txt
	@echo "Relatórios gerados: deps_report.txt, requirements_freeze.txt"
