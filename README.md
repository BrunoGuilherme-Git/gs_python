# ChuvaViva

## Descrição

O ChuvaViva é um sistema operacional climático urbano que transforma dados meteorológicos e de sensores IoT em decisões hiperlocais para enchentes e deslizamentos. A plataforma calcula riscos por bairro, classifica níveis de alerta e orienta a população com ações concretas em tempo real.

A proposta resume-se em uma frase: **cidade que escuta a chuva.**

---

## Objetivo

Demonstrar como dados dispersos — chuva acumulada, saturação do solo, declividade do terreno e impermeabilização urbana — podem ser transformados em informação acionável, rua por rua, auxiliando na evacuação de pessoas e no gerenciamento de abrigos durante eventos climáticos extremos.

---

## Tecnologias e bibliotecas utilizadas

| Tecnologia | Versão mínima | Finalidade |
|---|---|---|
| Python | 3.10+ | Linguagem principal |
| [questionary](https://github.com/tmbo/questionary) | qualquer | Menus interativos no terminal |
| [rich](https://github.com/Textualize/rich) | qualquer | Formatação colorida e painéis no terminal |
| logging | nativa | Geração de logs de execução em arquivo |
| datetime | nativa | Registro automático de data/hora nos reportes |

---

## Explicação do funcionamento

O sistema é iniciado via terminal e apresenta um menu principal com sete opções. Todas as operações são feitas por menus de seleção interativos — sem necessidade de digitar comandos. Os dados ficam em memória durante a execução.

### 1. Cadastros centrais

Gerenciamento completo (listar, adicionar, atualizar e remover) das quatro entidades do sistema:

| Cadastro | Campos |
|---|---|
| **Regiões** | Nome, risco predominante, score, população |
| **Sensores** | Tipo, status, região vinculada |
| **Abrigos** | Nome, endereço, capacidade, ocupação, região vinculada |
| **Reportes** | Tipo de ocorrência, região vinculada, data/hora (automática), finalizado (automático: `False`) |

Regras automáticas ao cadastrar:
- `data_hora` é preenchida com o momento atual.
- `finalizado` é sempre iniciado como `False`.
- Remover uma região remove automaticamente todos os sensores, abrigos e reportes vinculados a ela.

---

### 2. Processos

#### 2.1 Cálculo de risco da região

O usuário informa quatro parâmetros climáticos e o sistema retorna um **score de 0 a 10** com classificação de alerta e ação recomendada.

**Parâmetros de entrada:**
- Chuva acumulada (mm)
- Saturação do solo (%)
- Declividade do terreno (graus)
- Impermeabilização urbana (%)

**Critérios de pontuação por fator:**

| Fator | Peso | Faixas |
|---|---|---|
| Chuva acumulada | 35% | < 20 mm → 2 / < 50 → 4 / < 100 → 6 / < 200 → 8 / ≥ 200 → 10 |
| Saturação do solo | 25% | < 30% → 2 / < 60% → 5 / < 80% → 7 / ≥ 80% → 10 |
| Declividade | 25% | < 5° → 1 / < 15° → 4 / < 30° → 6 / < 45° → 8 / ≥ 45° → 10 |
| Impermeabilização | 15% | < 25% → 2 / < 50% → 4 / < 75% → 7 / ≥ 75% → 10 |

**Classificação do score final:**

| Score | Nível | Ação recomendada |
|---|---|---|
| 0,0 – 2,4 | BAIXO | Monitorar a situação |
| 2,5 – 4,9 | ATENÇÃO | Preparar kit de emergência |
| 5,0 – 7,4 | ALTO | Buscar local elevado e seguro |
| 7,5 – 10,0 | CRÍTICO | Evacuação imediata para o abrigo mais próximo disponível |

O score calculado é salvo no cadastro da região para uso nos relatórios.

---

#### 2.2 Finalizar reporte

Permite marcar um reporte de ocorrência como finalizado:

1. Usuário seleciona a região.
2. O sistema lista os reportes **pendentes** (não finalizados) dessa região.
3. Usuário seleciona qual reporte finalizar — o campo `finalizado` é marcado como `True`.
4. O sistema verifica se **todos** os reportes da região estão finalizados:
   - **Sim** → a ocupação de todos os abrigos da região é zerada, sinalizando que a emergência encerrou.
   - **Não** → informa quantos reportes ainda estão pendentes e mantém os abrigos como estão.

---

### 3. Relatórios

| Relatório | Descrição |
|---|---|
| **Sensores por status** | Filtra e lista sensores por status (ativo, inativo ou em manutenção) |
| **Ranking de bairros críticos** | Exibe o top 5 de regiões com maior score de risco |
| **Histórico de alertas** | Lista todos os reportes registrados em uma região selecionada |
| **Busca de abrigo disponível** | Exibe os abrigos com vagas disponíveis (ocupação < capacidade) em uma região |

---

### 4. Simulador de evento climático

O usuário define a **intensidade** e a **duração** de um evento de chuva. O sistema calcula a chuva acumulada e percorre todos os bairros cadastrados, recalculando o score de cada um com base no tipo de risco predominante da região, e lista quais entrariam em alerta.

**Intensidades disponíveis:**
- Chuva fraca — 2,5 mm/h
- Chuva moderada — 7,5 mm/h
- Chuva forte — 15 mm/h
- Chuva extrema — 25 mm/h

**Parâmetros de terreno por tipo de risco:**

| Risco predominante | Saturação | Declividade | Impermeabilização |
|---|---|---|---|
| Alagamento | 65% | 5° | 75% |
| Deslizamento | 75% | 35° | 40% |
| Ventos | 50% | 10° | 55% |

---

## Estrutura do projeto

```
gs_python/
├── main.py         # Loop principal e menu de navegação
├── data.py         # Dados iniciais (regiões, sensores, abrigos, reportes)
├── cadastros.py    # CRUD genérico para todas as entidades
├── processos.py    # Cálculo de risco, simulador e finalização de reporte
├── relatorios.py   # Geração dos quatro relatórios
├── utils.py        # Funções utilitárias (exibir tabela, converter tipos)
└── UI.py           # Configuração do terminal (Rich), paleta de cores e logger
```

Ao executar o sistema, um arquivo `chuvaviva.log` é gerado automaticamente na mesma pasta, registrando as principais ações realizadas (cadastros, cálculos de risco, reportes finalizados).

---

## Instalação e execução

**Pré-requisitos:** Python 3.10 ou superior.

**1. Clone o repositório ou baixe os arquivos.**

**2. Instale as dependências:**

```bash
pip install questionary rich
```

**3. Execute o sistema:**

```bash
python main.py
```

O menu principal será exibido no terminal e a navegação é feita inteiramente por setas e Enter.

---

## Exemplos de uso

### Calculando o risco de uma região

No menu principal, selecione **2. Processos**, depois **1. Calcular risco da região**.
Escolha a região desejada (ex: Itaquera) e informe os dados climáticos quando solicitado:

```
Chuva acumulada (mm) [0–500]: 130
Saturação do solo (%) [0–100]: 82
Declividade (graus) [0–90]: 28
Impermeabilização (%) [0–100]: 71

========================================================
  ANÁLISE DE RISCO — ITAQUERA
========================================================
  Chuva acumulada    :   130.0 mm   → 8/10  (peso 35%)
  Saturação do solo  :    82.0 %    → 10/10 (peso 25%)
  Declividade        :    28.0 °    → 6/10  (peso 25%)
  Impermeabilização  :    71.0 %    → 7/10  (peso 15%)
  ────────────────────────────────────────────────────
  SCORE FINAL  :  8.25/10   [CRÍTICO]
  AÇÃO         :  EVACUAÇÃO IMEDIATA! Dirija-se a: UBS Pinheiros — Rua dos Pinheiros, 410
========================================================
```

---

### Simulando um evento climático

No menu principal, selecione **4. Simulador de evento climático**.
Escolha a intensidade e informe a duração:

```
Intensidade da chuva: Chuva forte (15 mm/h)
Duração do evento (horas) [1–72]: 8

[SIMULAÇÃO] Chuva acumulada: 120.0 mm em 8h
========================================================
  REGIÃO                   SCORE  NÍVEL
  ────────────────────────────────────────────────────
  Centro                    7.90  CRÍTICO
  Vila Madalena             8.05  CRÍTICO
  Itaquera                  7.90  CRÍTICO
  Mooca                     6.65  ALTO
  Pinheiros                 7.90  CRÍTICO
========================================================

  Regiões em alerta: Centro, Vila Madalena, Itaquera, Mooca, Pinheiros
```

---

### Adicionando um novo abrigo

No menu principal, selecione **1. Cadastros centrais → Abrigos → Adicionar**.
Preencha os campos solicitados:

```
nome: Ginásio do Parque
endereco: Av. das Acácias, 900
capacidade: 200
ocupacao: 0
regiao_id: (selecione via menu — ex: Pinheiros)

→ Abrigo cadastrado com sucesso.
```

---

## Integrantes do grupo

| Nome | RM |
|---|---|
| Bruno Guilherme Gonçalves de Oliveira | RM573697 |
| Gabriel Cardoso de Sá Finzetto | RM571846 |
| Gabriel Luna Maia | RM570982 |
| João Lucas Magordo Rodrigues | RM572419 |
| Murilo Vieira dos Reis | RM573764 |
