from datetime import datetime

def formatar_valor(campo, valor):
    if campo == "data_hora":
        try:
            return datetime.fromisoformat(valor).strftime("%d/%m/%Y %H:%M")
        except:
            return str(valor)
    return str(valor)

def exibir_tabela(lista):
    if not lista:
        print("Nenhum item encontrado.")
        return
    campos = list(lista[0].keys())
    larguras = {}
    for c in campos:
        larguras[c] = max(len(c), max(len(formatar_valor(c, i[c])) for i in lista))

    separador = "+-" + "-+-".join("-" * larguras[c] for c in campos) + "-+"
    cabecalho  = "| " + " | ".join(c.upper().ljust(larguras[c]) for c in campos) + " |"

    print(separador)
    print(cabecalho)
    print(separador)
    for item in lista:
        linha = "| " + " | ".join(formatar_valor(c, item[c]).ljust(larguras[c]) for c in campos) + " |"
        print(linha)
    print(separador)
