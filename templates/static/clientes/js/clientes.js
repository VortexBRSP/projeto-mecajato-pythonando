function add_carro() {

    container = document.getElementById("form-carro")

    html = "<br> <div class='row'> <div class='col-md'> <input type='text' required='required' placeholder='carro' class='form-control' name='carro'> </div> <div class='col-md'><input type='text' required='required' placeholder='Placa' class='form-control' name='placa'> </div> </div>"

    container.innerHTML += html


}

function exibir_form(tipo) {
    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('att_cliente')

    if (tipo == '1') {
        att_cliente.style.display = 'none'
        add_cliente.style.display = 'block'

    } else if (tipo == '2') {
        att_cliente.style.display = 'block'
        add_cliente.style.display = 'none'
    }
}

function dados_cliente() {
    cliente = document.getElementById('cliente-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente = cliente.value
    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch("clientes/atualiza_cliente/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data

    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        document.getElementById('form-att-cliente').style.display = 'block'
        nome = document.getElementById('nome')
        nome.value = data['cliente']['nome']

        sobrenome = document.getElementById('sobrenome')
        sobrenome.value = data['cliente']['sobrenome']

        cpf = document.getElementById('cpf')
        cpf.value = data['cliente']['cpf']

        email = document.getElementById('email')
        email.value = data['cliente']['email']

        div_carros = document.getElementById('carros')
        div_carros.innerHTML = ""
        for (i = 0; i < data['carros'].length; i++) {
            div_carros.innerHTML += "<form action='/clientes/update_carro/" + data['carros'][i]['id'] + "' method='POST'><div class='row justify-content-md-center'><div class='col-md-auto'><input class='form-control' type='text' name='carro' value='" + data['carros'][i]['fields']['carro'] + "'</div></div><div class='col-md-auto'><input class='form-control' type='text' name='placa' value='" + data['carros'][i]['fields']['placa'] + "'/></div><div class='col-md-auto'><input class='btn btn-success' type='submit' value='Salvar'/></div><div class='col-md-auto'><a href='/clientes/excluir_carro/" + data['carros'][i]['id'] + "' class='btn btn-warning'>Excluir</a></div></div></div></form><br>"

        }
    })

}