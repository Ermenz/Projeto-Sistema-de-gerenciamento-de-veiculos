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
    return render_template('Aplication/index_aplication.html')

# Cadastro de Veículo
@app.route('/cadastrar_veiculo', methods=['POST'])
def cadastrar_veiculo():
    placa = request.form['placa']
    marca = request.form['marca']
    modelo = request.form['modelo']
    ano = request.form['ano']
    user_id = session.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO veiculos (placa, marca, modelo, ano, user_id) VALUES (?, ?, ?, ?, ?)",
                   (placa, marca, modelo, ano, user_id))
    conn.commit()
    conn.close()

    flash('Veículo cadastrado com sucesso!', 'success')
    return redirect(url_for('listar_veiculos'))

# Listagem de Veículos
@app.route('/listar_veiculos')
def listar_veiculos():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM veiculos WHERE user_id = ?", (user_id,))
    veiculos = cursor.fetchall()
    conn.close()
    print(f'Veículos retornados: {veiculos}')
    return render_template('List/index_list.html', veiculos=veiculos)

# Inicialização do servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
