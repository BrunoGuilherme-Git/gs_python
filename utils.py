from datetime import datetime
from UI import console, criar_painel, logger


def formatar_valor(campo, valor):
    if campo == "data_hora":
        try:
            return datetime.fromisoformat(valor).strftime("%d/%m/%Y %H:%M")
        except ValueError:
            logger.warning(f"Falha ao formatar data_hora: valor inválido '{valor}'")
            return str(valor)
    return str(valor)


def exibir_tabela(lista):
    if not lista:
        criar_painel("Nenhum item encontrado.", "Aviso", estilo="yellow")
        return

    campos = list(lista[0].keys())
    larguras = {}

    for c in campos:
        larguras[c] = max(len(c), max(len(formatar_valor(c, i[c])) for i in lista))

    separador = "+-" + "-+-".join("-" * larguras[c] for c in campos) + "-+"
    cabecalho = "| " + " | ".join(c.upper().ljust(larguras[c]) for c in campos) + " |"

    console.print(f"[cyan]{separador}[/cyan]")
    console.print(f"[bold white]{cabecalho}[/bold white]")
    console.print(f"[cyan]{separador}[/cyan]")

    for item in lista:
        linha = "| " + " | ".join(formatar_valor(c, item[c]).ljust(larguras[c]) for c in campos) + " |"
        linha_estilizada = linha.replace("|", "[cyan]|[/cyan]")
        console.print(linha_estilizada)

    console.print(f"[cyan]{separador}[/cyan]")


def converter(valor, tipo):
    try:
        if tipo == int:
            return int(valor)
        if tipo == float:
            return float(valor)
    except ValueError:
        return None
    return valor