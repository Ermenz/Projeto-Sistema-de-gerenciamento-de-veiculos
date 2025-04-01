import sqlite3

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Função para criar as tabelas no banco de dados
def criar_tabelas():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Criar tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
    ''')

    # Criar tabela de veículos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        ano INTEGER NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES usuarios(id)
    )
    ''')

    conn.commit()
    conn.close()
    print('Banco de dados e tabelas criados com sucesso!')

# Função para adicionar um novo usuário
def adicionar_usuario(nome, email, senha):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO usuarios (nome, email, senha) 
    VALUES (?, ?, ?)
    ''', (nome, email, senha))
    conn.commit()
    conn.close()

# Função para adicionar um novo veículo
def adicionar_veiculo(placa, marca, modelo, ano, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO veiculos (placa, marca, modelo, ano, user_id) 
    VALUES (?, ?, ?, ?, ?)
    ''', (placa, marca, modelo, ano, user_id))
    conn.commit()
    conn.close()

# Função para listar os veículos de um usuário
def listar_veiculos(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT placa, marca, modelo, ano 
    FROM veiculos 
    WHERE user_id = ?
    ''', (user_id,))
    veiculos = cursor.fetchall()
    conn.close()
    return veiculos

# Função para obter os dados de um usuário pelo seu ID
def obter_usuario_por_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM usuarios WHERE id = ?
    ''', (user_id,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario
