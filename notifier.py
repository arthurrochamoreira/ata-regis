from datetime import date, timedelta
import smtplib
import os
from email.message import EmailMessage
import datetime
import database
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', '25'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
FROM_ADDR = os.getenv('EMAIL_FROM', SMTP_USER)
TO_ADDRS = ["diatu@trf1.jus.br", "seae1@trf1.jus.br"]


def send_email(subject: str, body: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = FROM_ADDR
    msg['To'] = ', '.join(TO_ADDRS)
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        if SMTP_USER and SMTP_PASS:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)


def check_vigencias():
    """Verifica as atas com vigência próxima e envia e-mails."""
    hoje = date.today()
    limite = hoje + timedelta(days=90)
    for ata in database.get_all_atas():
        vigencia = datetime.datetime.strptime(ata['dataVigencia'], "%Y-%m-%d").date()
        if hoje <= vigencia <= limite:
            body = (
                f"Número da ARP: {ata['numeroAta']}\n"
                f"Documento SEI: {ata['documentoSei']}\n"
                f"Data de Vigência: {vigencia.strftime('%d/%m/%Y')}"
            )
            send_email("ARP próxima do vencimento", body)


def run_check():
    check_vigencias()

if __name__ == '__main__':
    run_check()
