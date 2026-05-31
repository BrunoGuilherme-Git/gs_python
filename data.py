# id, nome, risco_predominante, score, populacao
regioes = [
    {"id": 1, "nome": "Centro",        "risco_predominante": "alagamento",   "score": 8.5, "populacao": 10000},
    {"id": 2, "nome": "Vila Madalena", "risco_predominante": "deslizamento", "score": 7.2, "populacao": 31000},
    {"id": 3, "nome": "Itaquera",      "risco_predominante": "alagamento",   "score": 9.1, "populacao": 78000},
    {"id": 4, "nome": "Mooca",         "risco_predominante": "ventos",       "score": 4.3, "populacao": 25000},
    {"id": 5, "nome": "Pinheiros",     "risco_predominante": "alagamento",   "score": 6.8, "populacao": 37000},
]

# id, regiao_id, tipo, status
sensores = [
    {"id": 1, "regiao_id": 1, "tipo": "chuva",      "status": "ativo"},
    {"id": 2, "regiao_id": 2, "tipo": "solo",        "status": "ativo"},
    {"id": 3, "regiao_id": 3, "tipo": "chuva",       "status": "inativo"},
    {"id": 4, "regiao_id": 4, "tipo": "vento",       "status": "ativo"},
    {"id": 5, "regiao_id": 5, "tipo": "nivel_rio",   "status": "manutencao"},
]

# id, nome, endereco, capacidade, ocupacao
abrigos = [
    {"id": 1, "nome": "Abrigamento Central",      "endereco": "Rua Principal, 123",          "regiao_id": 2,     "capacidade": 100, "ocupacao": 50},
    {"id": 2, "nome": "Ginasio Vila Madalena",    "endereco": "Av. Henrique Schaumann, 55",  "regiao_id": 1,     "capacidade": 350, "ocupacao": 210},
    {"id": 3, "nome": "CRAS Itaquera",            "endereco": "Rua Itaquera, 800",           "regiao_id": 4,     "capacidade": 150, "ocupacao": 148},
    {"id": 4, "nome": "Centro Comunitario Mooca", "endereco": "Rua da Mooca, 230",           "regiao_id": 5,     "capacidade": 180, "ocupacao": 40},
    {"id": 5, "nome": "UBS Pinheiros",            "endereco": "Rua dos Pinheiros, 410",      "regiao_id": 3,     "capacidade": 100, "ocupacao": 75},
]

# id, regiao_id, tipo, data_hora
reportes = [
    {"id": 1, "regiao_id": 1, "tipo": "alagamento",    "data_hora": "2024-06-01T14:30:00"},
    {"id": 2, "regiao_id": 3, "tipo": "alagamento",    "data_hora": "2024-06-01T15:10:00"},
    {"id": 3, "regiao_id": 2, "tipo": "deslizamento",  "data_hora": "2024-06-02T08:45:00"},
    {"id": 4, "regiao_id": 5, "tipo": "alagamento",    "data_hora": "2024-06-02T11:00:00"},
    {"id": 5, "regiao_id": 4, "tipo": "ventos fortes", "data_hora": "2024-06-02T13:20:00"},
]

tipos_riscos = ["alagamento", "deslizamento", "ventos"]

status = ["ativo", "inativo", "manutencao"]