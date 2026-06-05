import questionary
from questionary import Choice

from data import *
from utils import exibir_tabela
from UI import console, render_header, criar_painel, PALETA

def menu_relatorios():
    render_header("Painel de Relatórios")

    escolha = questionary.select(
        "Escolha um relatório:",
        choices=[
            questionary.Choice(title="1. Sensores por status", value=1),
            questionary.Choice(title="2. Ranking de bairros mais críticos", value=2),
            questionary.Choice(title="3. Histórico de alertas emitidos", value=3),
            questionary.Choice(title="4. Busca de refúgio mais próximo", value=4),
            questionary.Choice(title="5. Voltar ao menu de cadastros", value=5)
        ]
    ).ask()

    return escolha


def exibir_relatorio(opcao):
    if opcao == 1:
        filtro = questionary.select(
            "Filtrar sensores por status:",
            choices=[Choice(title=item, value=item) for item in status]
        ).ask()

        if filtro is None:
            return

        filtrados = [sensor for sensor in sensores if sensor["status"] == filtro]

        render_header(f"Sensores com status '{filtro}'")
        exibir_tabela(filtrados)

    elif opcao == 2:
        top = sorted(regioes, key=lambda item: item["score"], reverse=True)[:5]

        render_header("Top 5 regiões com maior risco")
        exibir_tabela(top)

    elif opcao == 3:
        regiao_escolhida = questionary.select(
            "Escolha uma região:",
            choices=[Choice(title=item["nome"], value=item["id"]) for item in regioes]
        ).ask()

        if regiao_escolhida is None:
            return

        historico = [rp for rp in reportes if rp["regiao_id"] == regiao_escolhida]
        nome_regiao = next(regiao["nome"] for regiao in regioes if regiao["id"] == regiao_escolhida)

        render_header(f"Histórico de alertas — {nome_regiao}")
        exibir_tabela(historico)

    elif opcao == 4:
        regiao_escolhida = questionary.select(
            "Selecione o bairro:",
            choices=[Choice(title=regiao["nome"], value=regiao["id"]) for regiao in regioes]
        ).ask()

        if regiao_escolhida is None:
            return

        nome_regiao = next(regiao["nome"] for regiao in regioes if regiao["id"] == regiao_escolhida)
        disponiveis = [
            abrigo for abrigo in abrigos if
            abrigo["regiao_id"] == regiao_escolhida and abrigo["ocupacao"] < abrigo["capacidade"]
        ]

        render_header(f"Abrigos disponíveis em {nome_regiao}")
        exibir_tabela(disponiveis)