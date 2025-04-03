from database_setup import criar_tabelas, adicionar_usuario, adicionar_veiculo, listar_veiculos

# Criar tabelas (apenas uma vez)
criar_tabelas()

# Adicionar um usuário (se não existir)
adicionar_usuario("João", "joao@gmail.com", "senha123")

# Adicionar veículos para o usuário de ID 1
adicionar_veiculo("ABC-1234", "Toyota", "Corolla", 2020, 1)
adicionar_veiculo("XYZ-5678", "Honda", "Civic", 2019, 1)

# Listar os veículos do usuário com ID 1
veiculos = listar_veiculos(1)

print("Veículos cadastrados:")
for veiculo in veiculos:
    print(f"Placa: {veiculo['placa']}, Marca: {veiculo['marca']}, Modelo: {veiculo['modelo']}, Ano: {veiculo['ano']}")
