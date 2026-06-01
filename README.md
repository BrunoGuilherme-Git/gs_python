# ChuvaViva

## Descrição

O ChuvaViva é um sistema operacional climático urbano que transforma dados meteorológicos e de sensores IoT em decisões hiperlocais para enchentes e deslizamentos. A plataforma calcula riscos por bairro, classifica níveis de alerta e orienta a população com ações concretas em tempo real.

A proposta resume-se em uma frase: **cidade que escuta a chuva.**

## Objetivo

Demonstrar como dados dispersos — chuva acumulada, saturação do solo, declividade do terreno e impermeabilização urbana — podem ser transformados em informação acionável, rua por rua, auxiliando na evacuação de pessoas e no gerenciamento de abrigos durante eventos climáticos extremos.

## Sobre este protótipo

> Este repositório é um **protótipo em Python** que simula as funcionalidades centrais do ChuvaViva em ambiente de linha de comando (CLI). Ele não representa um sistema em produção, mas uma simulação funcional das principais telas, cálculos e fluxos do projeto real. Os dados utilizados são fictícios e servem apenas para fins de demonstração.

---

## Como executar

**Pré-requisitos:** Python 3.10+ e a biblioteca `questionary`.

```bash
pip install questionary
python main.py
```

---

## Opções do sistema

O menu principal oferece quatro módulos: **Cadastros**, **Processos**, **Relatórios** e informações sobre o projeto.

---

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

#### 2.2 Simulador de evento climático

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

Ao final, exibe a tabela com o score e o nível de alerta de cada região, destacando as que entrariam em estado **ALTO** ou **CRÍTICO**.

---

#### 2.3 Finalizar reporte

Permite marcar um reporte de ocorrência como finalizado. O fluxo funciona da seguinte forma:

1. Usuário seleciona a região.
2. O sistema lista os reportes **pendentes** (não finalizados) dessa região.
3. Usuário seleciona qual reporte finalizar — o campo `finalizado` é marcado como `True`.
4. O sistema verifica se **todos** os reportes da região estão finalizados:
   - **Sim** → a ocupação de todos os abrigos da região é zerada, sinalizando que a emergência encerrou.
   - **Não** → informa quantos reportes ainda estão pendentes e mantém os abrigos como estão.

---

### 3. Relatórios

Quatro relatórios de consulta disponíveis:

| Relatório | Descrição |
|---|---|
| **Sensores por status** | Filtra e lista sensores por status (ativo, inativo ou em manutenção) |
| **Ranking de bairros críticos** | Exibe o top 5 de regiões com maior score de risco |
| **Histórico de alertas** | Lista todos os reportes registrados em uma região selecionada |
| **Busca de abrigo disponível** | Exibe os abrigos com vagas disponíveis (ocupação < capacidade) em uma região |

---

## Estrutura de arquivos

```
gs_python/
├── main.py         # Loop principal e menu de navegação
├── data.py         # Dados iniciais (regiões, sensores, abrigos, reportes)
├── cadastros.py    # CRUD genérico para todas as entidades
├── processos.py    # Cálculo de risco, simulador e finalização de reporte
├── relatorios.py   # Geração dos quatro relatórios
└── utils.py        # Funções utilitárias (exibir tabela, converter tipos)
```
