.PHONY: build-up clean install run test help dev backup restore

# Cores para output
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

# Configurações
PYTHON=python3
PIP=pip3
VENV_DIR=.venv
SRC_DIR=src
BACKUP_DIR=backups
DATA_FILE=atas.json

# Comando de ajuda
help:
	@echo "$(GREEN)Ata de Registro de Preços - Sistema de Gerenciamento$(NC)"
	@echo ""
	@echo "$(YELLOW)Comandos disponíveis:$(NC)"
	@echo "  $(GREEN)build-up$(NC)     - Configura ambiente e executa aplicação"
	@echo "  $(GREEN)install$(NC)      - Instala dependências"
	@echo "  $(GREEN)run$(NC)          - Executa a aplicação"
	@echo "  $(GREEN)dev$(NC)          - Executa em modo desenvolvimento"
	@echo "  $(GREEN)test$(NC)         - Executa testes básicos"
	@echo "  $(GREEN)clean$(NC)        - Remove ambiente virtual"
	@echo "  $(GREEN)backup$(NC)       - Faz backup dos dados"
	@echo "  $(GREEN)restore$(NC)      - Restaura backup dos dados"
	@echo "  $(GREEN)help$(NC)         - Mostra esta ajuda"
	@echo ""

# Verifica se Python está instalado
check-python:
	@echo "$(YELLOW)Verificando Python...$(NC)"
	@which $(PYTHON) > /dev/null || (echo "$(RED)Python 3 não encontrado. Instale o Python 3.$(NC)" && exit 1)
	@echo "$(GREEN)Python 3 encontrado.$(NC)"
	@$(PYTHON) --version

# Cria o ambiente virtual
create-venv: check-python
	@echo "$(YELLOW)Configurando ambiente virtual...$(NC)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Criando ambiente virtual..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
	else \
		echo "$(GREEN)Ambiente virtual já existe.$(NC)"; \
	fi

# Instala as dependências
install: create-venv
	@echo "$(YELLOW)Instalando dependências...$(NC)"
	@$(VENV_DIR)/bin/pip install --upgrade pip
	@$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "$(GREEN)Dependências instaladas com sucesso.$(NC)"

# Executa a aplicação
run: install
	@echo "$(YELLOW)Executando aplicação...$(NC)"
	@cd $(SRC_DIR) && ../$(VENV_DIR)/bin/python main_gui.py

# Executa em modo desenvolvimento (com logs detalhados)
dev: install
	@echo "$(YELLOW)Executando em modo desenvolvimento...$(NC)"
	@echo "$(YELLOW)Logs detalhados habilitados$(NC)"
	@cd $(SRC_DIR) && PYTHONPATH=. ../$(VENV_DIR)/bin/python -u main_gui.py

# Comando principal
build-up: run

# Executa testes básicos
test: install
	@echo "$(YELLOW)Executando testes básicos...$(NC)"
	@$(VENV_DIR)/bin/python test_imports.py

# Faz backup dos dados
backup:
	@echo "$(YELLOW)Fazendo backup dos dados...$(NC)"
	@mkdir -p $(BACKUP_DIR)
	@if [ -f "$(DATA_FILE)" ]; then \
		cp $(DATA_FILE) $(BACKUP_DIR)/$(DATA_FILE).backup.$$(date +%Y%m%d_%H%M%S); \
		echo "$(GREEN)Backup criado em $(BACKUP_DIR)/$(NC)"; \
	else \
		echo "$(YELLOW)Arquivo de dados não encontrado.$(NC)"; \
	fi
	@if [ -d "$(SRC_DIR)" ]; then \
		tar -czf $(BACKUP_DIR)/src_backup_$$(date +%Y%m%d_%H%M%S).tar.gz $(SRC_DIR); \
		echo "$(GREEN)Backup do código fonte criado.$(NC)"; \
	fi

# Restaura backup dos dados
restore:
	@echo "$(YELLOW)Restaurando backup dos dados...$(NC)"
	@if [ -d "$(BACKUP_DIR)" ]; then \
		echo "Backups disponíveis:"; \
		ls -la $(BACKUP_DIR)/*.backup.* 2>/dev/null || echo "Nenhum backup encontrado"; \
	else \
		echo "$(RED)Diretório de backup não encontrado.$(NC)"; \
	fi

# Verifica estrutura do projeto
check-structure:
	@echo "$(YELLOW)Verificando estrutura do projeto...$(NC)"
	@echo "$(GREEN)Arquivos principais:$(NC)"
	@ls -la requirements.txt Makefile 2>/dev/null || echo "$(RED)Arquivos principais não encontrados$(NC)"
	@echo "$(GREEN)Diretório src:$(NC)"
	@ls -la $(SRC_DIR)/ 2>/dev/null || echo "$(RED)Diretório src não encontrado$(NC)"
	@echo "$(GREEN)Módulos:$(NC)"
	@ls -la $(SRC_DIR)/models/ $(SRC_DIR)/services/ $(SRC_DIR)/utils/ $(SRC_DIR)/forms/ 2>/dev/null || echo "$(RED)Alguns módulos não encontrados$(NC)"

# Limpa arquivos temporários
clean-temp:
	@echo "$(YELLOW)Limpando arquivos temporários...$(NC)"
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Arquivos temporários removidos.$(NC)"

# Limpa o ambiente
clean: clean-temp
	@echo "$(YELLOW)Removendo ambiente virtual...$(NC)"
	@rm -rf $(VENV_DIR)
	@echo "$(GREEN)Ambiente limpo.$(NC)"

# Reinstala tudo do zero
reinstall: clean install
	@echo "$(GREEN)Reinstalação concluída.$(NC)"

# Mostra informações do sistema
info:
	@echo "$(GREEN)Informações do Sistema:$(NC)"
	@echo "Python: $$($(PYTHON) --version 2>&1)"
	@echo "Pip: $$($(PIP) --version 2>&1)"
	@echo "Sistema: $$(uname -s)"
	@echo "Arquitetura: $$(uname -m)"
	@echo "Diretório atual: $$(pwd)"
	@echo "Ambiente virtual: $(VENV_DIR)"
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Status ambiente: $(GREEN)Criado$(NC)"; \
		echo "Pacotes instalados: $$($(VENV_DIR)/bin/pip list | wc -l) pacotes"; \
	else \
		echo "Status ambiente: $(RED)Não criado$(NC)"; \
	fi

# Atualiza dependências
update: install
	@echo "$(YELLOW)Atualizando dependências...$(NC)"
	@$(VENV_DIR)/bin/pip install --upgrade pip
	@$(VENV_DIR)/bin/pip install --upgrade -r requirements.txt
	@echo "$(GREEN)Dependências atualizadas.$(NC)"

# Gera relatório de dependências
deps-report: install
	@echo "$(YELLOW)Gerando relatório de dependências...$(NC)"
	@$(VENV_DIR)/bin/pip list > deps_report.txt
	@$(VENV_DIR)/bin/pip freeze > requirements_freeze.txt
	@echo "$(GREEN)Relatórios gerados: deps_report.txt, requirements_freeze.txt$(NC)"

