import smtplib
import email.message

def email():
    corpo_email = 'Email para redefinição de senha. ' \
    'Ete é apenas um email de exemplo para redefinir a sua senha.'

    msg = email.message.Message()
    msg['Subject'] = 'Redefinição de senha'
    #msg['From'] = f'remetente',   <= Aqui você coloca a variável que armazena o email do remetente
    msg['To'] = 'marcosandre1309@gmail.com'
    password = '' # <= Aqui você coloca a variável que armazena a senha do remetente
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('O email foi enviado!')

email()

