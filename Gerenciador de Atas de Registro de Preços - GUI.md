# Gerenciador de Atas de Registro de Preços - GUI

Uma aplicação Python com interface gráfica (GUI) para gerenciar atas de registro de preços, desenvolvida com Flet e SQLite. A interface é idêntica à versão web original, seguindo o design do Microsoft Planner.

## Características

- **Interface Gráfica Moderna**: Design inspirado no Microsoft Planner com cores e tipografia do Microsoft Fluent Design
- **Layout Kanban**: Organização visual das atas em três colunas (Vigentes, Próximas ao Vencimento, Vencidas)
- **Banco de Dados SQLite**: Armazenamento local seguro e eficiente
- **Responsivo**: Interface adaptável a diferentes tamanhos de janela
- **Funcionalidades Completas**: CRUD completo para atas, fornecedores, telefones, emails e itens

## Tecnologias Utilizadas

- **Python 3.11+**: Linguagem de programação principal
- **Flet**: Framework para criação de interfaces gráficas modernas
- **SQLite**: Banco de dados local
- **Microsoft Fluent Design**: Sistema de design para a interface

## Instalação

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone ou baixe os arquivos do projeto**:
   ```bash
   # Certifique-se de ter os arquivos:
   # - main_gui.py
   # - database.py
   # - README.md
   ```

2. **Instale as dependências**:
   ```bash
   pip install flet
   ```

3. **Execute a aplicação**:
   ```bash
   python main_gui.py
   ```

## Como Usar

### Iniciando a Aplicação

Execute o comando `python main_gui.py` no terminal. A aplicação abrirá em uma janela do navegador web, mas funcionará como uma aplicação desktop.

### Interface Principal

A interface principal apresenta:

- **Header**: Título da aplicação e botão "Nova Ata"
- **Painel de Controle**: Três colunas organizadas em formato Kanban
  - **Vigentes**: Atas com vigência superior a 90 dias
  - **Próximas ao Vencimento**: Atas que vencem em até 90 dias
  - **Vencidas**: Atas com vigência expirada

### Adicionando uma Nova Ata

1. Clique no botão **"Nova Ata"** no header
2. Preencha as informações básicas:
   - Número da Ata
   - Documento SEI
   - Objeto
   - Data de Assinatura
   - Data de Vigência
3. Adicione os dados do fornecedor:
   - Nome do Fornecedor
   - Telefones (clique em "Adicionar Telefone" para múltiplos)
   - E-mails (clique em "Adicionar E-mail" para múltiplos)
4. Adicione itens da ata:
   - Clique em "Adicionar Item"
   - Preencha descrição, quantidade e valor unitário
5. Clique em **"Salvar"**

### Editando uma Ata

1. Localize a ata desejada em uma das colunas
2. Clique no ícone de **edição** (lápis) no card da ata
3. Modifique os campos necessários
4. Clique em **"Salvar"**

### Excluindo uma Ata

1. Localize a ata desejada em uma das colunas
2. Clique no ícone de **exclusão** (lixeira) no card da ata
3. Confirme a exclusão no diálogo que aparece

### Visualização dos Cards

Cada card de ata exibe:
- **Título**: Objeto da ata
- **Identificação**: Número da ata e documento SEI
- **Status**: Badge colorido indicando o status (Vigente/Vence em breve/Vencida)
- **Progresso**: Barra de progresso baseada no tempo decorrido
- **Data de Vencimento**: Data de vigência formatada
- **Fornecedor**: Nome da empresa fornecedora
- **Ações**: Botões para editar e excluir

## Estrutura do Banco de Dados

O banco de dados SQLite (`atas_registro.db`) contém as seguintes tabelas:

### Tabela `atas`
- `id`: Chave primária
- `numeroAta`: Número da ata
- `documentoSei`: Documento SEI
- `objeto`: Descrição do objeto
- `dataAssinatura`: Data de assinatura
- `dataVigencia`: Data de vigência
- `fornecedor`: Nome do fornecedor
- `createdAt`: Data de criação
- `updatedAt`: Data de atualização

### Tabela `telefones`
- `id`: Chave primária
- `ata_id`: Referência à ata
- `telefone`: Número de telefone

### Tabela `emails`
- `id`: Chave primária
- `ata_id`: Referência à ata
- `email`: Endereço de e-mail

### Tabela `itens`
- `id`: Chave primária
- `ata_id`: Referência à ata
- `descricao`: Descrição do item
- `quantidade`: Quantidade
- `valor`: Valor unitário

## Arquitetura da Aplicação

### `main_gui.py`
Arquivo principal contendo:
- Classe `AtaApp`: Gerencia toda a interface e lógica da aplicação
- Configuração da interface usando Flet
- Handlers para eventos de usuário
- Integração com o banco de dados

### `database.py`
Módulo responsável por:
- Conexão com SQLite
- Criação e manutenção das tabelas
- Operações CRUD (Create, Read, Update, Delete)
- Funções utilitárias para manipulação de dados

## Funcionalidades Avançadas

### Categorização Automática
As atas são automaticamente categorizadas baseadas na data de vigência:
- **Vigentes**: Mais de 90 dias para vencer
- **Próximas ao Vencimento**: 90 dias ou menos para vencer
- **Vencidas**: Data de vigência já passou

### Barra de Progresso
Cada ata exibe uma barra de progresso calculada com base no tempo decorrido desde a assinatura até a vigência.

### Notificações
O sistema exibe notificações (snackbars) para:
- Confirmação de salvamento
- Confirmação de exclusão
- Mensagens de erro

### Validação de Dados
- Campos obrigatórios são validados
- Tratamento de erros para entradas inválidas
- Conversão automática de tipos de dados

## Personalização

### Cores e Temas
As cores seguem o Microsoft Fluent Design e podem ser modificadas na propriedade `self.colors` da classe `AtaApp`.

### Layout
O layout é responsivo e se adapta automaticamente ao tamanho da janela. As colunas se reorganizam em telas menores.

## Solução de Problemas

### Erro de Dependências
Se encontrar erros relacionados ao Flet:
```bash
pip install --upgrade flet
```

### Banco de Dados Corrompido
Se o banco de dados apresentar problemas:
1. Feche a aplicação
2. Delete o arquivo `atas_registro.db`
3. Reinicie a aplicação (um novo banco será criado)

### Problemas de Performance
Para melhor performance com muitas atas:
- Considere implementar paginação
- Adicione índices no banco de dados
- Otimize as consultas SQL

## Limitações

- A aplicação roda localmente (não é multi-usuário)
- Não possui backup automático
- Interface web requer navegador moderno
- Dependente da biblioteca Flet

## Desenvolvimento Futuro

Possíveis melhorias:
- Exportação para PDF/Excel
- Backup automático
- Filtros e busca avançada
- Relatórios e gráficos
- Integração com APIs externas
- Modo offline completo

## Suporte

Para problemas ou dúvidas:
1. Verifique se todas as dependências estão instaladas
2. Consulte os logs de erro no terminal
3. Verifique a documentação do Flet: https://flet.dev/

## Licença

Este projeto é fornecido como está, para fins educacionais e de demonstração.

