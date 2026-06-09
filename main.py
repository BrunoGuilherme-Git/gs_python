import questionary
from questionary import Choice
import os

from data import *
from cadastros import *
from relatorios import *
from processos import *
from UI import console, render_header, criar_painel, PALETA, logger

while True:
    try:
        render_header("ChuvaViva — Sistema Climático Urbano")

        escolha = questionary.select(
            "Escolha uma opção:",
            choices=[
                Choice(title="1. Cadastros centrais", value=1),
                Choice(title="2. Processos", value=2),
                Choice(title="3. Relatórios", value=3),
                Choice(title="4. Simulador de evento climático", value=4),
                Choice(title="5. Limpar o terminal", value=5),
                Choice(title="6. Sobre o projeto", value=6),
                Choice(title="7. Sair", value=7)
            ]
        ).ask()

        if escolha == 1:
            nome_lista = menu_cadastros()
            if nome_lista == "voltar":
                continue
            listas = {
                "regioes": regioes,
                "sensores": sensores,
                "abrigos": abrigos,
                "reportes": reportes,
            }
            lista = listas[nome_lista]
            opcoes_regioes = [Choice(title=regiao["nome"], value=regiao["id"]) for regiao in regioes]
            tipo_mapeados = {
                "regioes": {"risco_predominante": tipos_riscos},
                "reportes": {"tipo": tipos_riscos, "regiao_id": opcoes_regioes},
                "sensores": {"tipo": tipos_riscos, "status": status, "regiao_id": opcoes_regioes},
                "abrigos": {"regiao_id": opcoes_regioes},
            }
            opcao = menu_crud()
            executar_cadastro(lista, opcao, tipo_mapeados.get(nome_lista))

        elif escolha == 2:
            opcao = menu_processos()
            if opcao == 4:
                continue
            executar_processo(opcao)

        elif escolha == 3:
            opcao = menu_relatorios()
            if opcao == 5:
                continue
            exibir_relatorio(opcao)

        elif escolha == 4:
            executar_processo(2)

        elif escolha == 5:
            os.system('cls' if os.name == 'nt' else 'clear')

        elif escolha == 6:
            texto_sobre = (
                "O ChuvaViva é um sistema operacional climático urbano que transforma dados meteorológicos e de sensores IoT "
                "em decisões hiperlocais para enchentes e deslizamentos. A plataforma calcula riscos por bairro e classifica níveis "
                "de alerta (baixo, atenção, alto e crítico). Este protótipo em Python simula as funcionalidades centrais: cadastro "
                "de sensores, cálculo de risco e simulação de eventos climáticos. O objetivo é demonstrar como dados dispersos podem "
                "virar ação concreta, rua por rua. A proposta resume-se em uma frase: cidade que escuta a chuva."
            )
            console.print()
            criar_painel(texto_sobre, "SOBRE O PROJETO", estilo=PALETA["destaque"])
            console.print()

        elif escolha == 7:
            console.print("\n[bold yellow]Encerrando o programa. Até logo![/bold yellow]\n")
            break


    except KeyboardInterrupt:
        console.print("\n[bold yellow]Programa encerrado pelo usuário.[/bold yellow]\n")
        break
    except Exception as erro:
        logger.error(f"Erro inesperado no menu principal: {erro}")
        console.print(f"\n[red]Ocorreu um erro inesperado: {erro}[/red]\n")
