# Gerenciador de ARPs

Aplicativo desktop em Python utilizando **Flet** e banco de dados SQLite para cadastro e controle de Atas de Registro de Preços (ARP).

## Requisitos
- Python 3.12+
- Dependências listadas em `requirements.txt`

## Instalação
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração de e-mail
Crie um arquivo `.env` com as variáveis abaixo para envio das notificações:
```
SMTP_HOST=smtp.exemplo.com
SMTP_PORT=587
SMTP_USER=usuario
SMTP_PASS=senha
EMAIL_FROM=arp@example.com
```

## Execução
```
python main_gui.py
```
O agendador de verificação das vigências é iniciado através do script `scheduler.py`:
```
python scheduler.py
```

## Testes
Execute os testes unitários com:
```
pytest
```

## Empacotamento
Para gerar um executável utilize o PyInstaller:
```
pyinstaller app.spec
```
