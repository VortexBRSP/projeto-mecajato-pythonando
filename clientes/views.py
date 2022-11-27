from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Carro
import re
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import redirect


def clientes(request):
    if request.method == 'GET':
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')

        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'carros': zip(carros, placas)})

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(carros, placas)})

        cliente = Cliente(
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            cpf=cpf
        )

        cliente.save()

        for carro, placa in zip(carros, placas):
            car = Carro(carro=carro, placa=placa, cliente=cliente)
            car.save()
        return redirect(reverse('clientes')+f'?aba=att_clientes&id_cliente={id}')


def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=id_cliente)
    carros = Carro.objects.filter(cliente=cliente[0])
    cliente_json = json.loads(serializers.serialize('json', cliente))[
        0]['fields']
    carros_json = json.loads(serializers.serialize('json', carros))
    carros_json = [{'fields': carro['fields'], 'id': carro['pk']}
                   for carro in carros_json]
    data = {'cliente': cliente_json, 'carros': carros_json}
    return JsonResponse(data)


@csrf_exempt
def update_carro(request, id):
    nome_carro = request.POST.get('carro')
    placa = request.POST.get('placa')

    carro = Carro.objects.get(id=id)
    list_carros = Carro.objects.exclude(id=id).filter(placa=placa)
    if list_carros.exists():
        return HttpResponse('Placa já existente')

    carro.carro = nome_carro
    carro.placa = placa
    carro.save()
    return redirect(reverse('clientes')+f'?aba=att_clientes&id_cliente={id}')


@csrf_exempt
def excluir_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(reverse('clientes')+f'?aba=att_clientes&id_cliente={id}')
    except:
        # TODO: Exibir mensagem de erro
        return redirect(reverse('clientes')+f'?aba=att_clientes&id_cliente={id}')
