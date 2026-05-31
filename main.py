import questionary
import os

from data import *
from cadastros import *
from relatorios import *

while True:
    escolha = questionary.select(
        "Escolha uma opção:",
        choices=[
            Choice(title="1. Cadastros centrais", value=1),
            Choice(title="2. Processos", value=2),
            Choice(title="3. Relatórios", value=3),
            Choice(title="4. Limpar o terminal", value=4),
            Choice(title="5. Sobre o projeto", value=5),
            Choice(title="6. Sair", value=6)
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
        opcoes_regioes = [Choice(title=r["nome"], value=r["id"]) for r in regioes]
        choices_maps = {
            "regioes":  {"risco_predominante": tipos_riscos},
            "reportes": {"tipo": tipos_riscos, "regiao_id": opcoes_regioes},
            "sensores": {"tipo": tipos_riscos, "status": status, "regiao_id": opcoes_regioes},
            "abrigos":  {"regiao_id": opcoes_regioes},
        }
        opcao = menu_crud()
        executar_cadastro(lista, opcao, choices_maps.get(nome_lista))

    elif escolha == 3:
        opcao = menu_relatorios()
        if opcao == 5:
            continue
        exibir_relatorio(opcao)
        
    elif escolha == 4:
        os.system('cls' if os.name == 'nt' else 'clear')

    elif escolha == 5:
        print("\nO ChuvaViva é um sistema operacional climático urbano que transforma dados meteorológicos e de sensores IoT")
        print("em decisões hiperlocais para enchentes e deslizamentos. A plataforma calcula riscos por bairro e classifica níveis ")
        print("de alerta (baixo, atenção, alto e crítico). Este protótipo em Python simula as funcionalidades centrais: cadastro")
        print("de sensores, cálculo de risco e simulação de eventos climáticos. O objetivo é demonstrar como dados dispersos podem")
        print("virar ação concreta, rua por rua. A proposta resume-se em uma frase: cidade que escuta a chuva.\n")

    elif escolha == 6:
        print("Encerrando o programa.")
        break