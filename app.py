from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__,
            template_folder='src/pages',
            static_folder='src')

app.secret_key = os.urandom(24)

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Função para enviar e-mail
def enviar_email(email_destinatario, assunto, mensagem):
    try:
        email_remetente = 'projetoveiculos1@gmail.com'
        senha_remetente = 'txze elym zeqi pdqt'  # Senha do aplicativo

        msg = MIMEMultipart()
        msg['From'] = email_remetente
        msg['To'] = email_destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(mensagem, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_remetente, senha_remetente)
        server.sendmail(email_remetente, email_destinatario, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

# Página de Login
@app.route('/')
def login():
    return render_template('Login/index_login.html')

# Login POST
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['username']
    senha = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('aplicacao'))
    else:
        flash('Credenciais inválidas!', 'error')
        return redirect(url_for('login'))

# Página de Aplicação
@app.route('/aplicacao')
def aplicacao():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM veiculos")
    veiculos = cursor.fetchall()
    conn.close()
    return render_template('Aplication/index_aplication.html', veiculos=veiculos)

# Cadastro de Veículo
@app.route('/cadastrar_veiculo', methods=['POST'])
def cadastrar_veiculo():
    placa = request.form['placa']
    marca = request.form['marca']
    modelo = request.form['modelo']
    ano = request.form['ano']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO veiculos (placa, marca, modelo, ano) VALUES (?, ?, ?, ?)",
                   (placa, marca, modelo, ano))
    conn.commit()
    conn.close()

    flash('Veículo cadastrado com sucesso!', 'success')
    return redirect(url_for('aplicacao'))

# Esqueci a Senha
@app.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form['email']
        assunto = 'Recuperação de Senha'
        mensagem = '<p>Você solicitou a recuperação de senha. Clique no link para redefinir: <a href="http://127.0.0.1:5000/reset-senha">Redefinir Senha</a></p>'

        if enviar_email(email, assunto, mensagem):
            flash('E-mail enviado com sucesso!', 'success')
        else:
            flash('Erro ao enviar o e-mail.', 'error')

        return redirect(url_for('esqueci_senha'))

    return render_template('ForgetPassword/index_forget.html')

# Redefinir Senha
@app.route('/reset-senha', methods=['GET', 'POST'])
def reset_senha():
    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        email = request.form['email']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET senha = ? WHERE email = ?", (nova_senha, email))
        conn.commit()
        conn.close()

        flash('Senha redefinida com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('ForgetPassword/reset_senha.html')

# Inicialização do servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
