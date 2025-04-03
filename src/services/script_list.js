function editarVeiculo(id) {
    const row = document.getElementById(`veiculo-${id}`);
    const marca = row.querySelector('.marca');
    const modelo = row.querySelector('.modelo');
    const ano = row.querySelector('.ano');
    const placa = row.querySelector('.placa');

    // Habilitar a edição
    marca.contentEditable = true;
    modelo.contentEditable = true;
    ano.contentEditable = true;
    placa.contentEditable = true;

    // Alterar o botão para "Salvar"
    const botaoEditar = row.querySelector('.botao-editar');
    botaoEditar.innerText = "Salvar";
    botaoEditar.onclick = function () { salvarVeiculo(id); };
}

function salvarVeiculo(id) {
    const row = document.getElementById(`veiculo-${id}`);
    const marca = row.querySelector('.marca').textContent;
    const modelo = row.querySelector('.modelo').textContent;
    const ano = row.querySelector('.ano').textContent;
    const placa = row.querySelector('.placa').textContent;

    console.log("ID do veículo:", id);
    console.log("Dados enviados:", { marca, modelo, ano, placa });

    fetch(`/editar_veiculo/${id}`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify({ 
            marca: marca,
            modelo: modelo,
            ano: ano,
            placa: placa
        })
    }).then(response => {
        console.log("Resposta do servidor:", response);
        if (response.ok) {
            alert('Veículo atualizado com sucesso!');
            desabilitarEdicao(row);
        } else {
            return response.json().then(data => {
                alert(`Erro ao atualizar o veículo: ${data.message || "Erro desconhecido"}`);
            });
        }
    }).catch(error => {
        console.error("Erro na requisição:", error);
        alert("Erro ao atualizar o veículo. Verifique o console para mais detalhes.");
    });
}

function desabilitarEdicao(row) {
    const marca = row.querySelector('.marca');
    const modelo = row.querySelector('.modelo');
    const ano = row.querySelector('.ano');
    const placa = row.querySelector('.placa');

    // Desabilitar a edição
    marca.contentEditable = false;
    modelo.contentEditable = false;
    ano.contentEditable = false;
    placa.contentEditable = false;

    // Alterar o botão para "Editar"
    const botaoEditar = row.querySelector('.botao-editar');
    botaoEditar.innerText = "Editar";
    botaoEditar.onclick = function () { editarVeiculo(row.id.split('-')[1]); };
}

function removerVeiculo(id) {
    fetch(`/remover_veiculo/${id}`, {
        method: 'POST'
    }).then(response => {
        if (response.ok) {
            alert('Veículo removido com sucesso!');
            location.reload();
        } else {
            alert('Erro ao remover o veículo.');
        }
    }).catch(error => {
        console.error("Erro ao remover o veículo:", error);
        alert("Erro ao remover o veículo. Verifique o console para mais detalhes.");
    });
}
