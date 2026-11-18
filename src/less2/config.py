"""Constantes de pontuação. FONTE ÚNICA DA VERDADE: nenhum outro arquivo deve repetir estas listas."""
SEED = 42

LESS_MAX = 6      # escala 1-6 -> inversão: 7 - x
DERS_MAX = 5      # escala 1-5 -> inversão: 6 - x

REV_LESS = [4, 6, 14, 15, 19, 24, 25, 26]
REV_DERS = [1, 2, 6, 7, 8, 10, 17, 20, 22, 24, 34]  # pontuação da DERS original (11 itens)

DERS_SUBSCALES = {
    "Nao_aceitacao": [11, 12, 21, 23, 25, 29],
    "Metas": [13, 18, 20, 26, 33],
    "Impulsos": [3, 14, 19, 24, 27, 32],
    "Consciencia": [2, 6, 8, 10, 17, 34],
    "Estrategias": [15, 16, 22, 28, 30, 31, 35, 36],
    "Clareza": [1, 4, 5, 7, 9],
}
ERQ_REAPPRAISAL = [1, 3, 5, 7, 8, 10]
ERQ_SUPPRESSION = [2, 4, 6, 9]
DASS = {
    "Depressao": [3, 5, 10, 13, 16, 17, 21],
    "Ansiedade": [2, 4, 7, 9, 15, 19, 20],
    "Estresse": [1, 6, 8, 11, 12, 14, 18],
}
DASS_MODERATE_CUT = {"Depressao": 14, "Ansiedade": 10, "Estresse": 19}  # soma x 2

LESS_14 = {
    "Invalidacao": [6, 12], "Incompreensibilidade": [3, 7], "Culpa": [2, 10],
    "Visao_simplista": [23, 28], "Desvalorizacao_valores": [14, 26], "Perda_controle": [5, 17],
    "Entorpecimento": [11, 20], "Racionalidade": [13, 27], "Duracao": [9, 19],
    "Baixo_consenso": [1, 25], "Nao_aceitacao": [18, 24], "Ruminacao": [16, 22],
    "Baixa_expressao": [4, 15], "Culpabilizacao": [8, 21],
}
LESS_FACTORS = {  # carga primária na AFE; escore = média não ponderada dos itens
    "F1": [3, 5, 7, 9, 10, 16, 17, 20, 22], "F2": [14, 21, 23, 26, 28], "F3": [11, 13, 27],
    "F4": [2, 18, 19], "F5": [1, 4, 6, 8, 12, 15, 24, 25],
}
LESS_CORE24_DROP = [11, 19, 26, 28]

N_ITEMS = {"ders": 36, "eqr": 10, "less": 28, "dass": 21}
ALL_ITEMS = [f"{p}_{i}" for p, n in N_ITEMS.items() for i in range(1, n + 1)]
