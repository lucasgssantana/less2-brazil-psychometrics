# Relatório de verificação (agregados; sem dados individuais)

Execução: `run_all.py` sobre `USP.CSV` e `BANCO_DE_DADOS_REFORMADO.csv`, semente 42, 9 testes `pytest` aprovados.

## Fluxo amostral (regra: 95 itens completos + gênero 0/1)

265 identificadores nos arquivos de trabalho → 25 abandonos (1 sem item; 13 após a DERS; 9 após DERS e ERQ; 2 durante/após a LESS-II) + 1 erro de exportação + 1 item ausente pontual → **238**. Os ids comuns aos dois arquivos (240) são idênticos item a item (0 células divergentes). Os 238 e seus itens são idênticos aos de `resultado_final_clusters.csv`.

## Reproduzido

n, sexo, idade, α (LESS 0,87; DERS 0,95; subescalas 0,83–0,91; ERQ 0,84/0,72; DASS 0,86–0,90), KMO (Pearson) 0,873, Bartlett χ²(378) = 2.300,0, Shapiro–Wilk p = 0,21, normas (Tabela 8), grupos conhecidos (Tabela 7), R² e ΔR² (Tabela 6), DIF por item (item 18: ΔR² = 0,025; p = 0,005), limiares de poder (0,025; 0,050; 0,037), atrito (n = 25 e subconjunto de 23), Tabela 3 a partir das cargas (ω 0,916; ωH 0,839; ECV 0,588; PUC 0,788).

## Divergências

Ver `AUDITORIA_SCRIPTS_LEGADOS.md`, seção final.

## Não verificado

Policórica, AFE, análise paralela e CFA (R não executado); IC bootstrap exatos (dependem da semente/implementação); família do Holm na Tabela 5.
