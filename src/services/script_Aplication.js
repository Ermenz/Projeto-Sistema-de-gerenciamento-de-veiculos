const apiUrl = "http://localhost:5000";  // Altere para o endereço correto do seu Flask

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

    const user_id = 1;  // Substitua com o user_id do usuário logado

    const response = await fetch(`${apiUrl}/api/adicionar_veiculo`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ placa, marca, modelo, ano, user_id })
    });

    const data = await response.json();

    if (response.ok) {
        alert(data.message);
        listarCarros();  // Atualizar a lista de carros após o cadastro
    } else {
        alert("Erro ao cadastrar veículo: " + data.message);
    }
}

// Função para listar os veículos
async function listarCarros() {
    const user_id = 1;  // Substitua com o user_id do usuário logado

    const response = await fetch(`${apiUrl}/api/listar_veiculos?user_id=${user_id}`);
    const veiculos = await response.json();

    const listaCarros = document.getElementById("lista-carros");
    listaCarros.innerHTML = "";  // Limpar a lista antes de adicionar novos itens

    veiculos.forEach(veiculo => {
        const div = document.createElement("div");
        div.textContent = `Placa: ${veiculo.placa}, Marca: ${veiculo.marca}, Modelo: ${veiculo.modelo}, Ano: ${veiculo.ano}`;
        listaCarros.appendChild(div);
    });
}
