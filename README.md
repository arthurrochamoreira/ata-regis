# 📝 Sistema de Atas de Registro de Preços

Sistema desktop desenvolvido em Python com Flet para gerenciar Atas de Registro de Preços, conforme especificação do TRF1.

## 🚀 Características Principais

### ✨ Interface Moderna
- Interface gráfica desktop com Flet
- Design inspirado no PNCP
- Responsiva e intuitiva
- Suporte a tema claro e escuro
- Navegação em abas (Dashboard, Atas e Vencimentos)

### 📊 Painel de Controle
- **Gráfico de Pizza**: Situação das atas (Vigentes, A Vencer, Vencidas)
- **Cards de Resumo**: Estatísticas principais
- **Indicador de Urgência**: Alertas visuais para atas críticas
- **Gráfico de Valores**: Distribuição financeira por status
- **Gráfico Mensal**: Vencimentos por mês

### 🔍 Funcionalidades de Gestão
- **CRUD Completo**: Criar, visualizar, editar e excluir atas
- **Validação Robusta**: Máscaras e validações em tempo real
- **Busca Avançada**: Filtros por status e busca textual
- **Formulários Dinâmicos**: Campos para itens, telefones e emails

### 📧 Sistema de Alertas Automáticos
- **Alertas Programados**: D-90, D-60, D-30, D-15, D-7, D-1
- **Relatórios Automáticos**: Semanal e mensal
- **Monitoramento Contínuo**: Agendador em background
- **Histórico de Alertas**: Controle de envios

## 📋 Campos da Ata

### 📄 Dados Principais
- **documento_sei**: `str` - Formato: `00000.000000/0000-00`
- **numero_ata**: `str` - Formato: `XXXX/AAAA`
- **data_vigencia**: `date` - Data de vencimento
- **objeto**: `str` - Descrição do objeto

### 🏢 Fornecedor
- **fornecedor**: `str` - Nome da empresa
- **telefones_fornecedor**: `list[str]` - Formato: `(XX) XXXXX-XXXX`
- **emails_fornecedor**: `list[str]` - Emails válidos

### 🧾 Itens
- **descricao**: `str` - Descrição do item
- **quantidade**: `int` - Quantidade positiva
- **valor**: `float` - Valor unitário

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**: Linguagem principal
- **Flet 0.22.0**: Framework para interface desktop
- **Dataclasses**: Modelagem de dados
- **Threading**: Agendamento de tarefas
- **JSON**: Persistência de dados
- **SQLite**: Alternativa de banco de dados

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.11 ou superior
- Make (opcional, mas recomendado)

### 🚀 Execução Rápida
```bash
# Clone ou baixe o projeto
cd ata_registro_precos_app

# Execute com Make (recomendado)
make build-up

# Ou execute manualmente
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cd src && ../.venv/bin/python main_gui.py
```

### 📋 Comandos Disponíveis

```bash
make help          # Mostra todos os comandos
make build-up       # Configura e executa aplicação
make install        # Instala dependências
make run            # Executa aplicação
make dev            # Executa em modo desenvolvimento
make test           # Executa testes básicos
make clean          # Remove ambiente virtual
make backup         # Faz backup dos dados
make restore        # Lista backups disponíveis
make info           # Mostra informações do sistema
```

## 📁 Estrutura do Projeto

```
ata_registro_precos_app/
├── src/                    # Código fonte
│   ├── models/            # Modelos de dados
│   │   ├── __init__.py
│   │   └── ata.py         # Classes Ata e Item
│   ├── services/          # Serviços de negócio
│   │   ├── __init__.py
│   │   ├── ata_service.py # CRUD das atas
│   │   ├── sqlite_ata_service.py # CRUD usando SQLite
│   │   └── alert_service.py # Alertas automáticos
│   ├── utils/             # Utilitários
│   │   ├── __init__.py
│   │   ├── validators.py  # Validações e formatação
│   │   ├── email_service.py # Serviço de email
│   │   ├── chart_utils.py # Utilitários de gráficos
│   │   └── scheduler.py   # Agendador de tarefas
│   ├── forms/             # Formulários
│   │   ├── __init__.py
│   │   └── ata_form.py    # Formulário de ata
│   └── main_gui.py        # Interface principal
├── requirements.txt       # Dependências
├── Makefile              # Automação
├── test_imports.py       # Testes
├── README.md             # Documentação
└── atas.json             # Dados (criado automaticamente)
```

## 🎯 Funcionalidades Implementadas

### ✅ Interface Principal
- [x] Tabela interativa de atas
- [x] Filtros por status (Vigentes, A Vencer, Vencidas, Todas)
- [x] Campo de busca em tempo real
- [x] Botões de ação (Visualizar, Editar, Excluir)

### ✅ Formulários
- [x] Formulário completo para criação/edição
- [x] Validações em tempo real
- [x] Máscaras automáticas (SEI, telefone, número da ata)
- [x] Campos dinâmicos (itens, telefones, emails)

### ✅ Painel Gráfico
- [x] Gráfico de pizza com status das atas
- [x] Cards de resumo com estatísticas
- [x] Indicador de urgência
- [x] Gráfico de valores por status
- [x] Gráfico de vencimentos mensais

### ✅ Sistema de Alertas
- [x] Verificação automática diária (09:00)
- [x] Relatório semanal (segunda-feira 08:00)
- [x] Relatório mensal (dia 1º às 07:00)
- [x] Alertas programados (D-90 até vencimento)
- [x] Histórico de alertas

### ✅ Ferramentas
- [x] Menu de ferramentas na interface
- [x] Verificação manual de alertas
- [x] Geração manual de relatórios
- [x] Teste de configuração de email
- [x] Status do sistema

## 📧 Sistema de Email (Simulado)

Por enquanto, o sistema simula o envio de emails através de prints no console. Os emails são direcionados para:
- `diatu@trf1.jus.br`
- `seae1@trf1.jus.br`

### Tipos de Alertas
- **D-90**: 90 dias antes do vencimento
- **D-60**: 60 dias antes do vencimento
- **D-30**: 30 dias antes do vencimento
- **D-15**: 15 dias antes do vencimento
- **D-7**: 7 dias antes do vencimento
- **D-1**: 1 dia antes do vencimento
- **VENCIMENTO**: No dia do vencimento
- **PÓS-VENCIMENTO**: Até 30 dias após vencimento

## 🧪 Testes

Execute os testes para verificar a integridade do sistema:

```bash
make test
```

Os testes verificam:
- ✅ Importações de todos os módulos
- ✅ Criação de objetos básicos
- ✅ Validadores e formatadores
- ✅ Serviços principais

## 💾 Backup e Restore

### Fazer Backup
```bash
make backup
```
Cria backup dos dados e código fonte em `backups/`

### Restaurar Backup
```bash
make restore
```
Lista backups disponíveis para restauração manual

## 🔧 Desenvolvimento

### Modo Desenvolvimento
```bash
make dev
```
Executa com logs detalhados habilitados

### Limpeza
```bash
make clean          # Remove ambiente virtual
make clean-temp     # Remove arquivos temporários
make reinstall      # Reinstala do zero
```

### Informações do Sistema
```bash
make info           # Mostra configurações
make deps-report    # Gera relatório de dependências
```

## 📊 Dados Mockados

O sistema vem com dados de exemplo para demonstração:

1. **Ata 0016/2024** - Micro Tipo I (Vigente)
2. **Ata 0015/2024** - Material de Escritório (A Vencer)
3. **Ata 0014/2024** - Equipamentos de TI (Vencida)

## 🎨 Design e UX

### Diretrizes de Layout
- Sistema de grid de 8px
- Padding interno padrão: 16px
- Espaçamento entre seções: 24-32px
- Altura dos campos: 48-56px

### Cores
- **Verde**: Atas vigentes
- **Laranja**: Atas a vencer
- **Vermelho**: Atas vencidas
- **Azul**: Elementos de interface

## 🚨 Tratamento de Erros

- Validações em tempo real nos formulários
- Mensagens de erro claras e específicas
- Tratamento de exceções em operações críticas
- Logs detalhados para debugging

## 📈 Performance

- Carregamento otimizado de dados
- Atualização incremental da interface
- Agendador eficiente em background
- Gestão de memória para histórico de alertas

## 🔒 Segurança

- Validação rigorosa de entrada de dados
- Sanitização de campos de texto
- Controle de acesso a arquivos
- Tratamento seguro de exceções

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Execute os testes: `make test`
4. Faça commit das mudanças
5. Abra um Pull Request

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Verifique os logs no console
- Execute `make info` para diagnóstico
- Use `make test` para verificar integridade

## 📄 Licença

Este projeto foi desenvolvido para o TRF1 conforme especificação fornecida.

---

**Desenvolvido com ❤️ usando Python + Flet**

