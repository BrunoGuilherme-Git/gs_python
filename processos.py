import questionary
from questionary import Choice

from data import *
from utils import *

verde    = "\033[32m"
amarelo  = "\033[33m"
laranja  = "\033[91m"
vermelho = "\033[31m"
reset    = "\033[0m"
negrito  = "\033[1m"

cor_por_nivel = {
    "BAIXO":   verde,
    "ATENÇÃO": amarelo,
    "ALTO":    laranja,
    "CRÍTICO": vermelho,
}

intensidades = {
    "Chuva fraca    (2.5 mm/h)":  2.5,
    "Chuva moderada (7.5 mm/h)":  7.5,
    "Chuva forte    (15 mm/h)":  15.0,
    "Chuva extrema  (25 mm/h)":  25.0,
}

params_por_risco = {
    "alagamento":   {"saturacao": 65, "declividade":  5, "impermeabilizacao": 75},
    "deslizamento": {"saturacao": 75, "declividade": 35, "impermeabilizacao": 40},
    "ventos":       {"saturacao": 50, "declividade": 10, "impermeabilizacao": 55},
}
params_default = {"saturacao": 60, "declividade": 15, "impermeabilizacao": 60}


def menu_processos():
    escolha = questionary.select(
        "Escolha: ",
        choices=[
            questionary.Choice(title="1. Cálcular risco da região",     value=1),
            questionary.Choice(title="2. Simulador de evento climático", value=2),
            questionary.Choice(title="3. Finalizar reporte",             value=3),
            questionary.Choice(title="4. Voltar ao menu principal",      value=4),
        ]
    ).ask()
    return escolha


def pontuacao_chuva(chuva):
    if chuva < 20:
        return 2
    elif chuva < 50:
        return 4
    elif chuva < 100:
        return 6
    elif chuva < 200:
        return 8
    else:
        return 10


def pontuacao_saturacao(saturacao):
    if saturacao < 30:
        return 2
    elif saturacao < 60:
        return 5
    elif saturacao < 80:
        return 7
    else:
        return 10


def pontuacao_declividade(declividade):
    if declividade < 5:
        return 1
    elif declividade < 15:
        return 4
    elif declividade < 30:
        return 6
    elif declividade < 45:
        return 8
    else:
        return 10


def pontuacao_impermeabilizacao(impermeabilizacao):
    if impermeabilizacao < 25:
        return 2
    elif impermeabilizacao < 50:
        return 4
    elif impermeabilizacao < 75:
        return 7
    else:
        return 10


def calcular_score(chuva, saturacao, declividade, impermeabilizacao):
    score_chuva             = pontuacao_chuva(chuva)
    score_saturacao         = pontuacao_saturacao(saturacao)
    score_declividade       = pontuacao_declividade(declividade)
    score_impermeabilizacao = pontuacao_impermeabilizacao(impermeabilizacao)

    score_final = (
        score_chuva             * 0.35 +
        score_saturacao         * 0.25 +
        score_declividade       * 0.25 +
        score_impermeabilizacao * 0.15
    )

    if score_final > 10:
        score_final = 10

    return round(score_final, 2)


def classificar_nivel(score):
    if score < 2.5:
        return "BAIXO"
    elif score < 5.0:
        return "ATENÇÃO"
    elif score < 7.5:
        return "ALTO"
    else:
        return "CRÍTICO"


def acao_recomendada(nivel, regiao_id):
    if nivel == "BAIXO":
        return "Monitorar a situação. Nenhuma ação imediata necessária."
    elif nivel == "ATENÇÃO":
        return "Fique em alerta. Prepare kit de emergência e evite áreas de risco."
    elif nivel == "ALTO":
        return "Procure local elevado e seguro. Evite deslocamentos desnecessários."
    else:
        abrigo_disponivel = None
        for abrigo in abrigos:
            if abrigo["regiao_id"] == regiao_id and abrigo["ocupacao"] < abrigo["capacidade"]:
                abrigo_disponivel = abrigo
                break

        if abrigo_disponivel:
            return f"EVACUAÇÃO IMEDIATA! Dirija-se a: {abrigo_disponivel['nome']} — {abrigo_disponivel['endereco']}"
        return "EVACUAÇÃO IMEDIATA! Procure o abrigo mais próximo com vagas disponíveis."


def pedir_float(prompt, minimo, maximo):
    while True:
        valor = input(f"  {prompt} [{minimo}–{maximo}]: ")
        try:
            numero = float(valor)
            if numero >= minimo and numero <= maximo:
                return numero
            print(f"    Valor deve estar entre {minimo} e {maximo}.")
        except ValueError:
            print("    Digite um número válido.")


def exibir_resultado(regiao, chuva, saturacao, declividade, impermeabilizacao):
    score_chuva             = pontuacao_chuva(chuva)
    score_saturacao         = pontuacao_saturacao(saturacao)
    score_declividade       = pontuacao_declividade(declividade)
    score_impermeabilizacao = pontuacao_impermeabilizacao(impermeabilizacao)
    score                   = calcular_score(chuva, saturacao, declividade, impermeabilizacao)
    nivel                   = classificar_nivel(score)
    cor                     = cor_por_nivel[nivel]
    acao                    = acao_recomendada(nivel, regiao["id"])

    print(f"\n{'='*56}")
    print(f"  ANÁLISE DE RISCO — {regiao['nome'].upper()}")
    print(f"{'='*56}")
    print(f"  Chuva acumulada    : {chuva:>7.1f} mm   → {score_chuva}/10  (peso 35%)")
    print(f"  Saturação do solo  : {saturacao:>7.1f} %    → {score_saturacao}/10  (peso 25%)")
    print(f"  Declividade        : {declividade:>7.1f} °     → {score_declividade}/10  (peso 25%)")
    print(f"  Impermeabilização  : {impermeabilizacao:>7.1f} %    → {score_impermeabilizacao}/10  (peso 15%)")
    print(f"  {'─'*52}")
    print(f"  {negrito}SCORE FINAL  :{reset} {cor}{negrito} {score:>5.2f}/10   [{nivel}]{reset}")
    print(f"  {negrito}AÇÃO         :{reset} {cor}{acao}{reset}")
    print(f"{'='*56}\n")

    return score


def executar_processo(opcao):
    if opcao == 1:
        if not regioes:
            print("Nenhuma região cadastrada.")
            return

        regiao_id = questionary.select(
            "Selecione a região:",
            choices=[Choice(title=regiao["nome"], value=regiao["id"]) for regiao in regioes]
        ).ask()
        if regiao_id is None:
            return

        regiao_selecionada = None
        for regiao in regioes:
            if regiao["id"] == regiao_id:
                regiao_selecionada = regiao
                break

        print(f"\nInforme os dados climáticos para {regiao_selecionada['nome']}:")
        chuva             = pedir_float("Chuva acumulada (mm)",  0, 500)
        saturacao         = pedir_float("Saturação do solo (%)", 0, 100)
        declividade       = pedir_float("Declividade (graus)",    0,  90)
        impermeabilizacao = pedir_float("Impermeabilização (%)", 0, 100)

        score = exibir_resultado(regiao_selecionada, chuva, saturacao, declividade, impermeabilizacao)
        regiao_selecionada["score"] = score

    elif opcao == 2:
        intensidade = questionary.select(
            "Intensidade da chuva:",
            choices=[Choice(title=nome, value=valor) for nome, valor in intensidades.items()]
        ).ask()
        if intensidade is None:
            return

        duracao     = pedir_float("Duração do evento (horas)", 1, 72)
        chuva_total = intensidade * duracao

        print(f"\n[SIMULAÇÃO] Chuva acumulada: {chuva_total:.1f} mm em {duracao:.0f}h")
        print(f"{'='*56}")
        print(f"  {'REGIÃO':<24} {'SCORE':>6}  NÍVEL")
        print(f"  {'─'*52}")

        regioes_em_alerta = []
        for regiao in regioes:
            if regiao["risco_predominante"] in params_por_risco:
                params = params_por_risco[regiao["risco_predominante"]]
            else:
                params = params_default

            score = calcular_score(
                chuva_total,
                params["saturacao"],
                params["declividade"],
                params["impermeabilizacao"],
            )
            nivel = classificar_nivel(score)
            cor   = cor_por_nivel[nivel]
            print(f"  {regiao['nome']:<24} {score:>6.2f}  {cor}{nivel}{reset}")

            if nivel == "ALTO" or nivel == "CRÍTICO":
                regioes_em_alerta.append(regiao["nome"])

        print(f"{'='*56}")
        if regioes_em_alerta:
            nomes = ", ".join(regioes_em_alerta)
            print(f"\n  {vermelho}{negrito}Regiões em alerta:{reset} {nomes}\n")
        else:
            print(f"\n  {verde}Nenhuma região entra em alerta para este evento.{reset}\n")

    elif opcao == 3:
        if not regioes:
            print("Nenhuma região cadastrada.")
            return

        regiao_id = questionary.select(
            "Selecione a região:",
            choices=[Choice(title=regiao["nome"], value=regiao["id"]) for regiao in regioes]
        ).ask()
        if regiao_id is None:
            return

        nome_regiao = ""
        for regiao in regioes:
            if regiao["id"] == regiao_id:
                nome_regiao = regiao["nome"]
                break

        reportes_da_regiao = []
        for reporte in reportes:
            if reporte["regiao_id"] == regiao_id:
                reportes_da_regiao.append(reporte)

        reportes_pendentes = []
        for reporte in reportes_da_regiao:
            if reporte["finalizado"] == False:
                reportes_pendentes.append(reporte)

        if not reportes_pendentes:
            print(f"\nTodos os reportes de {nome_regiao} já estão finalizados.")
            return

        reporte_id = questionary.select(
            "Selecione o reporte para finalizar:",
            choices=[Choice(title=str(reporte), value=reporte["id"]) for reporte in reportes_pendentes]
        ).ask()
        if reporte_id is None:
            return

        for reporte in reportes:
            if reporte["id"] == reporte_id:
                reporte["finalizado"] = True
                break

        print(f"\nReporte #{reporte_id} finalizado.")

        todos_finalizados = True
        for reporte in reportes_da_regiao:
            if reporte["finalizado"] == False:
                todos_finalizados = False
                break

        if todos_finalizados:
            abrigos_da_regiao = []
            for abrigo in abrigos:
                if abrigo["regiao_id"] == regiao_id:
                    abrigos_da_regiao.append(abrigo)

            for abrigo in abrigos_da_regiao:
                abrigo["ocupacao"] = 0

            print(f"Todos os reportes de {nome_regiao} finalizados — ocupação dos abrigos zerada.\n")
            exibir_tabela(abrigos_da_regiao)
        else:
            pendentes_restantes = 0
            for reporte in reportes_da_regiao:
                if reporte["finalizado"] == False:
                    pendentes_restantes += 1
            print(f"Ainda há {pendentes_restantes} reporte(s) pendente(s) em {nome_regiao}. Abrigos mantidos.\n")
