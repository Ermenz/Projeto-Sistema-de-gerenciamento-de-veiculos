from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from src.services.send_email import send_email
from database_setup import adicionar_veiculo, listar_veiculos

app = Flask(__name__,
            template_folder='src/pages',
            static_folder='src')

app.secret_key = os.urandom(24)

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def login():
    return render_template('Login/index_login.html')

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

@app.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form['email']
        subject = "Recuperação de Senha"
        message = "Clique no link para redefinir sua senha: http://127.0.0.1:5000/reset-senha"

        if send_email(email, subject, message):
            flash('E-mail enviado com sucesso!', 'success')
        else:
            flash('Erro ao enviar o e-mail.', 'error')

        return redirect(url_for('esqueci_senha'))

    return render_template('ForgetPassword/index_forget.html')

if __name__ == '__main__':
    app.run(debug=True)
