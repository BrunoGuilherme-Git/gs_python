import questionary
from questionary import Choice
from datetime import datetime

from utils import *
from data import *

def adicionar(lista, item):
    ultimo_id = lista[-1]["id"] if lista else 0
    item["id"] = ultimo_id + 1
    lista.append(item)
    return lista

def remover(lista, id):
    for i in lista[:]:
        if i['id'] == id:
            lista.remove(i)
    if lista is regioes:
        for i in sensores[:]:
            if i['regiao_id'] == id:
                sensores.remove(i)
        for i in reportes[:]:
            if i['regiao_id'] == id:
                reportes.remove(i)
        for i in abrigos[:]:
            if i['regiao_id'] == id:
                abrigos.remove(i)
    return lista

def atualizar(lista, id, novos_dados):
    for i in lista:
        if i['id'] == id:
            i.update(novos_dados)
    return lista

def listar(lista):
    exibir_tabela(lista)

def menu_cadastros():
    escolha = questionary.select(
        "Escolha um cadastro para gerenciar:",
        choices=[
            questionary.Choice(title="1. Regiões", value="regioes"),
            questionary.Choice(title="2. Sensores", value="sensores"),
            questionary.Choice(title="3. Abrigos", value="abrigos"),
            questionary.Choice(title="4. Reportes", value="reportes"),
            questionary.Choice(title="5. Voltar ao menu principal", value="voltar")
        ]
    ).ask()
    
    return escolha

def menu_crud():
        escolha = questionary.select(
            "Escolha uma ação:",
            choices=[
                questionary.Choice(title="1. Listar", value=1),
                questionary.Choice(title="2. Adicionar", value=2),
                questionary.Choice(title="3. Atualizar", value=3),
                questionary.Choice(title="4. Remover", value=4),
                questionary.Choice(title="5. Voltar ao menu de cadastros", value=5)
            ]
        ).ask()

        return escolha

def pedir_valor(campo, referencia, opcoes=None):
    if opcoes:
        return questionary.select(f"{campo}:", choices=opcoes).ask()
    tipo = type(referencia)
    while True:
        valor = input(f"{campo}: ")
        if tipo in (int, float):
            convertido = converter(valor, tipo)
            if convertido is not None:
                return convertido
            print(f"  '{campo}' deve ser um número {'inteiro' if tipo == int else 'decimal'}.")
        elif valor.strip() == "":
            print(f"  '{campo}' não pode ser vazio.")
        else:
            return valor

def pedir_valor_opcional(campo, referencia, opcoes=None):
    if opcoes:
        ja_sao_choices = isinstance(opcoes[0], Choice)
        itens = opcoes if ja_sao_choices else [Choice(title=o, value=o) for o in opcoes]
        choices = [Choice(title="(manter atual)", value=None)] + itens
        return questionary.select(f"{campo}:", choices=choices).ask()
    tipo = type(referencia)
    while True:
        valor = input(f"{campo} (enter para manter): ")
        if valor == "":
            return None
        if tipo in (int, float):
            convertido = converter(valor, tipo)
            if convertido is not None:
                return convertido
            print(f"  '{campo}' deve ser um número {'inteiro' if tipo == int else 'decimal'}.")
        else:
            return valor

def executar_cadastro(lista, opcao, choices_map=None):
    choices_map = choices_map or {}

    if opcao == 1:
        listar(lista)

    elif opcao == 2:
        referencia = lista[0] if lista else {}
        campos = [key for key in referencia.keys() if key != "id"]
        novo_item = {}
        for campo in campos:
            if campo == "data_hora":
                novo_item[campo] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            else:
                novo_item[campo] = pedir_valor(campo, referencia[campo], choices_map.get(campo))
        adicionar(lista, novo_item)

    elif opcao == 3:
        if not lista:
            print("Nenhum item cadastrado.")
            return
        choices = [Choice(title=str(i), value=i["id"]) for i in lista]
        id_alvo = questionary.select("Selecione o item a atualizar:", choices=choices).ask()
        if id_alvo is None:
            return
        item_alvo = next(i for i in lista if i["id"] == id_alvo)
        campos = [key for key in item_alvo.keys() if key != "id"]
        novos_dados = {}
        for campo in campos:
            valor = pedir_valor_opcional(campo, item_alvo[campo], choices_map.get(campo))
            if valor is not None:
                novos_dados[campo] = valor
        atualizar(lista, id_alvo, novos_dados)

    elif opcao == 4:
        if not lista:
            print("Nenhum item cadastrado.")
            return
        choices = [Choice(title=str(i), value=i["id"]) for i in lista]
        id_alvo = questionary.select("Selecione o item a remover:", choices=choices).ask()
        if id_alvo is None:
            return
        remover(lista, id_alvo)
