const apiUrl = "http://localhost:5000";  // Endereço do servidor Flask

// Função para adicionar um veículo
async function adicionarCarro() {
    const placa = document.getElementById("placa").value;
    const marca = document.getElementById("marca").value;
    const modelo = document.getElementById("modelo").value;
    const ano = document.getElementById("ano").value;

    if (!placa || !marca || !modelo || !ano) {
        alert("Todos os campos devem ser preenchidos!");
        return;
    }

    const response = await fetch(`${apiUrl}/cadastrar_veiculo`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ placa, marca, modelo, ano })
    });

    const data = await response.json();

    if (response.ok) {
        alert("Veículo cadastrado com sucesso!");
        listarCarros();  // Atualizar a lista de carros após o cadastro
    } else {
        alert("Erro ao cadastrar veículo: " + data.message);
    }
}

// Função para listar os veículos
async function listarCarros() {
    const response = await fetch(`${apiUrl}/listar_veiculos`);
    const veiculos = await response.json();

    const listaCarros = document.getElementById("lista-carros");
    listaCarros.innerHTML = "";  // Limpar a lista antes de adicionar novos itens

    veiculos.forEach(veiculo => {
        const div = document.createElement("div");
        div.textContent = `Placa: ${veiculo.placa}, Marca: ${veiculo.marca}, Modelo: ${veiculo.modelo}, Ano: ${veiculo.ano}`;
        listaCarros.appendChild(div);
    });
}
