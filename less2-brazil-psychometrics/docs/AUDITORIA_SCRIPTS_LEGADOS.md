# Auditoria dos scripts legados do projeto

Critério: um script só entra no repositório do manuscrito da LESS-II se (a) pertence a esse manuscrito, (b) usa a mesma pontuação do texto e (c) roda sem editar caminhos. **Nenhum script legado atende aos três.** Os de cálculo foram substituídos por `src/less2/` + `scripts/`.

## Pertencem ao artigo de K-means (outro repositório)

| Script | Situação | Problema |
|---|---|---|
| `z-score.py` | **Corrigir antes de usar** | DERS: inverte só os itens 1, 2, 6, 7, 8, 10, 17 e 22; **não inverte 20, 24 e 34** (a pontuação original inverte 11 itens). Com os 11 itens, α da DERS = 0,954 e média = 96,65; com os 8, α = 0,930 e média = 94,59. Metas, Impulsos e Consciência (usadas como entrada do K-means) ficam distorcidas |
| `cluster.py` | **Corrigir** | `KMeans(random_state=42)` sem `n_init`: no sklearn atual vale `n_init='auto'` (= 1 com k-means++). `PCA.PY`, `Metodo_cotovelo_silhouette.py` e `auditoria_final.py` usam `n_init=10`. Teste: com K = 2, as soluções coincidem (ARI = 1,00); com K = 3, **ARI = 0,887** (tamanhos 66/78/94 com `n_init=10` contra 95/61/82 no arquivo). O gráfico PCA e a referência do bootstrap não mostram a solução tabelada |
| `auditoria_final.py` | Usável após fixar `n_init` | Bootstrap e GMM corretos; depende da solução de `cluster.py` |
| `robusto_py.py` | Quebrado | Lê `df['Fenotipo']`, coluna inexistente em `resultado_final_clusters.csv` (a coluna é `cluster_k3`); lê o CSV com `,` em vez de `;` |
| `N_tamanho_de_efeito.py` | Quebrado | Abre `resultado_final_clusters - Copia.csv` com `sep=","` |
| `N_tamanho_de_efeito copy.py` | Lixo | Só imprime colunas |
| `medias_efect.py`, `passo.py`, `poshoc.py` | Usáveis | Mann–Whitney, Kruskal–Wallis e Bonferroni (0,016) corretos; r bisserial por postos = \|1 − 2U/(n₀n₁)\| |
| `gerar_matriz.py`, `Metodo_cotovelo_silhouette.py`, `PCA.PY` | Usáveis após fixar `n_init` | Dependem de `matriz_pura_clusterizacao.csv` |
| `random_forest_xai.py`, `random_forest_gemini.py` | Usáveis | Excluir caminhos fixos e declarar a semente; evitam vazamento (usam itens, não escores) |

## Obsoletos ou inválidos (não publicar)

| Script | Problema |
|---|---|
| `Pipline_processamento_de_dados…py` | Imputa **todos** os valores ausentes pela mediana (contradiz o 238 por casos completos); inverte DERS com `7 − x` numa escala 1–5 e inclui o item 28 (que não é reverso); mapeia subescalas da LESS com pares de itens diferentes dos de Leahy |
| `limpeza.py`, `clusters.py`, `resultados.py`, `estatistica.py`, `auditoria_casos.py`, `verifcar.py` | Pipeline antigo com 4 variáveis (`ders_total`, `reavaliacao`, `supressao`, `less_total`) **sem itens reversos**. Resultado 80/69/89 não é o K = 3 final |
| `preparar_banco.py` | Nome de arquivo com espaços; limpa decimais "corrompidos" de uma exportação anterior; não alimenta nenhuma tabela atual |
| `play.py`, `teste.py` | Contêm só `pip install …` |
| `z-score copy.py` | Calculadora de exemplo; nada a ver com o projeto |

## Divergências entre manuscrito v19 e recálculo (ver também `VERIFICACAO.md`)

1. **Tabela 5**, DERS Metas × F3: manuscrito "0,04 ns", recálculo **−0,20** (significativo após Holm); DERS Consciência × F4: manuscrito "0,03 ns", recálculo **0,20**. A versão anterior (PDF v2) trazia −0,20 e 0,20. A frase "F3 … nenhuma subescala da DERS (|ρ| ≤ 0,07)" fica incorreta se o recálculo estiver certo.
2. Tabela 5: F1 × DERS total 0,78 (recálculo 0,77) e F1 × ERQ reavaliação −0,34 (recálculo −0,33): diferença ≤ 0,01, provavelmente arredondamento ou ponderação.
3. Tabela 6, AUC: ansiedade 0,773 → 0,784 (recálculo 0,775 → 0,783) e estresse 0,835 → 0,844 (recálculo 0,829 → 0,838); depende do modelo exato.
