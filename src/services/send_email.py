import smtplib
from email.message import EmailMessage
import os

def send_email(to_email, subject, message):
    from_email = "projetoveiculos1@gmail.com"
    from_password = "txzeelymzeqipdqt"  # Senha de aplicativo (use a correta aqui)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(message)

    try:
        # Configuração do servidor SMTP (Gmail)
        smtp_server = "smtp.gmail.com"
        port = 587

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
            print("E-mail enviado com sucesso!")
            return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
