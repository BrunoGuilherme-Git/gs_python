from fpdf import FPDF

# Times New Roman via arquivos do Windows (nao usa a fonte core do fpdf)
FONT      = r"C:\Windows\Fonts\times.ttf"
FONT_BOLD = r"C:\Windows\Fonts\timesbd.ttf"
FONT_IT   = r"C:\Windows\Fonts\timesi.ttf"
FONT_BI   = r"C:\Windows\Fonts\timesbi.ttf"

# ABNT: margem esq/sup 3 cm, dir/inf 2 cm (em mm)
ML, MR, MT, MB = 30, 20, 30, 20


class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-MB)
        self.set_font("TNR", "", 10)
        self.cell(0, 10, str(self.page_no()), align="R")


def make_pdf():
    pdf = PDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=MB)
    pdf.add_font("TNR",  "",   FONT)
    pdf.add_font("TNR",  "B",  FONT_BOLD)
    pdf.add_font("TNR",  "I",  FONT_IT)
    pdf.add_font("TNR",  "BI", FONT_BI)
    pdf.set_margins(ML, MT, MR)

    LARGURA = pdf.w - ML - MR  # largura util: 210 - 30 - 20 = 160 mm

    # ------------------------------------------------------------------ helpers

    def secao(num, titulo):
        pdf.ln(6)
        pdf.set_font("TNR", "B", 12)
        pdf.cell(0, 7, f"{num}  {titulo.upper()}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    def subsecao(num, titulo):
        pdf.set_font("TNR", "B", 12)
        pdf.cell(0, 7, f"{num}  {titulo}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    def paragrafo(texto):
        pdf.set_font("TNR", "", 12)
        pdf.set_x(ML + 12.5)
        pdf.multi_cell(LARGURA - 12.5, 7, texto, align="J")
        pdf.ln(2)

    def italico(texto):
        pdf.set_font("TNR", "I", 12)
        pdf.set_x(ML + 12.5)
        pdf.cell(0, 7, texto, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    def imagem(legenda):
        pdf.ln(2)
        pdf.set_fill_color(240, 240, 240)
        pdf.set_draw_color(150, 150, 150)
        pdf.set_font("TNR", "I", 10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(LARGURA, 30, f"[ IMAGEM: {legenda} ]",
                 border=1, fill=True, align="C",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
        pdf.set_draw_color(0, 0, 0)
        pdf.ln(5)

    def tabela(cabecalhos, linhas, larguras):
        # cabecalho
        pdf.set_font("TNR", "B", 10)
        pdf.set_fill_color(200, 200, 200)
        for texto, w in zip(cabecalhos, larguras):
            pdf.cell(w, 6, texto, border=1, fill=True)
        pdf.ln()
        # linhas
        pdf.set_font("TNR", "", 10)
        for linha in linhas:
            x_ini = pdf.l_margin
            y_ini = pdf.get_y()
            # altura da linha: maior numero de linhas entre as celulas
            altura_max = 6
            for texto, w in zip(linha, larguras):
                n = len(pdf.multi_cell(w, 6, texto, border=0,
                                       dry_run=True, output="LINES"))
                if n * 6 > altura_max:
                    altura_max = n * 6
            # verifica quebra de pagina
            if y_ini + altura_max > pdf.h - MB:
                pdf.add_page()
                y_ini = pdf.get_y()
            # renderiza cada celula
            for texto, w in zip(linha, larguras):
                pdf.set_xy(x_ini, y_ini)
                pdf.multi_cell(w, 6, texto, border=1)
                x_ini += w
            pdf.set_xy(pdf.l_margin, y_ini + altura_max)
        pdf.ln(4)

    # ================================================================= CAPA ===
    pdf.add_page()

    pdf.set_font("TNR", "B", 12)
    pdf.multi_cell(0, 7,
        "FACULDADE DE INFORMATICA E ADMINISTRACAO PAULISTA - FIAP",
        align="C")
    pdf.ln(2)
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Curso: Engenharia de Software",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Disciplina: Computational Thinking with Python",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Professor: Jose Roberto Candido da Silva",
             align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(35)

    pdf.set_font("TNR", "B", 14)
    pdf.cell(0, 9, "CHUVAVIVA", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("TNR", "B", 12)
    pdf.multi_cell(0, 7,
        "Sistema de Monitoramento de Risco Climatico Urbano",
        align="C")
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.cell(0, 7, "Global Solution 2026 - Space Connect",
             align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(35)

    pdf.set_font("TNR", "", 12)
    integrantes = [
        ("Bruno Guilherme Goncalves de Oliveira", "RM573697"),
        ("Gabriel Cardoso de Sa Finzetto",        "RM571846"),
        ("Gabriel Luna Maia",                     "RM570982"),
        ("Joao Lucas Magordo Rodrigues",           "RM572419"),
        ("Murilo Vieira dos Reis",                 "RM573764"),
    ]
    for nome, rm in integrantes:
        pdf.cell(0, 7, f"{nome}  -  {rm}",
                 align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(35)
    pdf.cell(0, 7, "Sao Paulo", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "2026",      align="C", new_x="LMARGIN", new_y="NEXT")

    # =========================================================== CONTEUDO ====
    pdf.add_page()

    # --- 1. Descricao da Solucao (minimo 10, maximo 20 linhas)
    secao("1", "Descricao da Solucao Proposta")

    paragrafo(
        "A Global Solution 2026 - Space Connect propoe aplicar tecnologia espacial a "
        "desafios reais da humanidade. O ChuvaViva e um sistema de monitoramento de "
        "risco climatico urbano que simula como dados de sensores IoT e satelites "
        "meteorologicos podem ser transformados em decisoes hiperlocais para prevencao "
        "de enchentes e deslizamentos. O problema abordado e a ausencia de ferramentas "
        "que traduzam dados dispersos em orientacoes concretas para a populacao e "
        "gestores de emergencia. A solucao integra quatro variaveis climaticas - chuva "
        "acumulada, saturacao do solo, declividade e impermeabilizacao urbana - e "
        "calcula um score de risco de 0 a 10 por bairro, classificado em quatro niveis: "
        "BAIXO, ATENCAO, ALTO e CRITICO. Os objetivos sao: centralizar o cadastro de "
        "regioes, sensores, abrigos e reportes; calcular e atualizar o score de risco "
        "dinamicamente; simular eventos climaticos sobre todos os bairros; gerir "
        "abrigos durante emergencias; e fornecer relatorios analiticos. As principais "
        "funcionalidades incluem CRUD completo das quatro entidades, calculo ponderado "
        "de risco, simulador de evento, finalizacao de reportes com zeragem automatica "
        "de abrigos, e quatro relatorios de consulta. Cidade que escuta a chuva."
    )

    # --- 2. Funcionalidades
    secao("2", "Explicacao das Funcionalidades")

    subsecao("2.1", "Menu Principal e Navegacao")
    paragrafo(
        "O programa e executado via terminal e apresenta um menu interativo com seis "
        "opcoes: Cadastros Centrais, Processos, Relatorios, Limpar Terminal, Sobre o "
        "Projeto e Sair. Apos a execucao de qualquer funcionalidade, o sistema retorna "
        "automaticamente ao menu principal por meio de um laco while True."
    )

    imagem("Menu principal exibido no terminal")

    subsecao("2.2", "Cadastros Centrais")
    paragrafo(
        "Gerenciamento completo (listar, adicionar, atualizar e remover) de quatro "
        "entidades: Regioes, Sensores, Abrigos e Reportes. Campos automaticos: "
        "data_hora e finalizado sao preenchidos no momento do cadastro. A remocao "
        "de uma regiao exclui em cascata todos os seus sensores, abrigos e reportes."
    )

    tabela(
        ["Entidade", "Campos gerenciados"],
        [
            ["Regioes",  "nome, risco_predominante, score, populacao"],
            ["Sensores", "tipo, status, regiao_id"],
            ["Abrigos",  "nome, endereco, capacidade, ocupacao, regiao_id"],
            ["Reportes", "tipo, regiao_id, data_hora (auto), finalizado (auto)"],
        ],
        [40, LARGURA - 40]
    )

    imagem("Listagem de regioes cadastradas (opcao Listar do menu Cadastros)")

    subsecao("2.3", "Processos")

    italico("a) Calculo de Risco da Regiao")
    paragrafo(
        "O usuario seleciona uma regiao e informa quatro parametros climaticos. O "
        "sistema calcula o score final ponderado (chuva 35%, saturacao 25%, "
        "declividade 25%, impermeabilizacao 15%), classifica o nivel de alerta e "
        "exibe a acao recomendada. O score e salvo na regiao."
    )

    tabela(
        ["Score", "Nivel", "Acao recomendada"],
        [
            ["0,0 - 2,4", "BAIXO",   "Monitorar a situacao."],
            ["2,5 - 4,9", "ATENCAO", "Preparar kit de emergencia."],
            ["5,0 - 7,4", "ALTO",    "Buscar local elevado e seguro."],
            ["7,5 - 10,0","CRITICO", "Evacuacao imediata para abrigo disponivel."],
        ],
        [28, 26, LARGURA - 54]
    )

    imagem("Resultado do calculo de risco: score, nivel e acao recomendada")

    italico("b) Simulador de Evento Climatico")
    paragrafo(
        "O usuario escolhe a intensidade da chuva e a duracao em horas. O sistema "
        "percorre todos os bairros, recalcula o score de cada um e exibe tabela com "
        "nivel de alerta, destacando regioes em estado ALTO ou CRITICO."
    )

    imagem("Tabela do simulador com score e nivel de alerta por regiao")

    italico("c) Finalizacao de Reporte")
    paragrafo(
        "O usuario seleciona uma regiao e encerra um reporte pendente. Se todos os "
        "reportes da regiao estiverem finalizados, a ocupacao dos abrigos e zerada "
        "automaticamente, sinalizando o fim da emergencia."
    )

    imagem("Finalizacao de reporte e zeragem da ocupacao dos abrigos")

    subsecao("2.4", "Relatorios")
    paragrafo(
        "Quatro consultas analiticas disponiveis: sensores por status, ranking dos "
        "cinco bairros mais criticos por score, historico de alertas por regiao e "
        "busca de abrigos com vagas disponiveis."
    )

    imagem("Exemplo de relatorio: ranking de bairros criticos")

    # --- 3. Estrutura de Arquivos
    secao("3", "Estrutura de Arquivos do Projeto")

    tabela(
        ["Arquivo", "Responsabilidade"],
        [
            ["main.py",       "Loop principal, menu de navegacao e despacho das funcionalidades."],
            ["data.py",       "Dados iniciais: listas de regioes, sensores, abrigos e reportes."],
            ["cadastros.py",  "CRUD generico para todas as entidades e menus de cadastro."],
            ["processos.py",  "Calculo de risco, simulador de evento e finalizacao de reporte."],
            ["relatorios.py", "Geracao dos quatro relatorios analiticos."],
            ["utils.py",      "Funcoes utilitarias: tabelas formatadas e conversao de tipos."],
        ],
        [38, LARGURA - 38]
    )

    pdf.output("documentacao.pdf")
    print("PDF gerado com sucesso: documentacao.pdf")


make_pdf()
