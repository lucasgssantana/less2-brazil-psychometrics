# LESS-II em adultos brasileiros: código de análise

Código que reproduz as tabelas e figuras do manuscrito *"A Escala de Esquemas Emocionais de Leahy-II em adultos brasileiros: fator geral forte, fatores específicos fracos e validade de critério frente a depressão, ansiedade e estresse"* (n = 238).

> **Dados:** os dados individuais **não são públicos** (termos do consentimento). Este repositório contém apenas código. Quem tiver autorização deve colocar `USP.CSV` e `BANCO_DE_DADOS_REFORMADO.csv` em `data/raw/`.
> *English note:* analysis code only; individual-level data are not shared.

## Uso

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp /caminho/privado/USP.CSV /caminho/privado/BANCO_DE_DADOS_REFORMADO.csv data/raw/
python run_all.py --raw-dir data/raw --out-dir outputs
pytest -q                      # testes-âncora contra os valores do manuscrito
# Em R (local):
Rscript r/01_polychoric_efa.R && Rscript r/02_cfa_models.R
python scripts/07_bifactor_indices_from_loadings.py
```

## Estrutura

```
src/less2/config.py            # ÚNICA fonte de listas de itens, itens reversos e subescalas
src/less2/data.py              # leitura, união USP/REFORMADO, regra de inclusão e motivos de exclusão
src/less2/scoring.py           # recodificação e escores
src/less2/stats_utils.py       # Holm, alfa, Spearman bootstrap, d de Cohen, bisserial por postos
src/less2/bifactor_indices.py  # ω, ωH, ECV, PUC, ωHS
scripts/01..07_*.py            # um script por bloco de resultados
r/                             # policórica/AFE/CFA (lavaan, WLSMV)
tests/                         # pytest: configuração, índices bifatoriais, valores-âncora
docs/                          # auditoria dos scripts legados e relatório de verificação
```

## Decisões de pontuação (documentadas em `config.py`)

- LESS-II: itens 4, 6, 14, 15, 19, 24, 25 e 26 invertidos (7 − x).
- DERS: itens 1, 2, 6, 7, 8, 10, 17, 20, 22, 24 e 34 invertidos (6 − x), pontuação da escala original.
- DASS-21: soma das subescalas × 2; limiares ≥ moderado: 14, 10 e 19.
- Escores dos fatores F1–F5: média não ponderada dos itens com carga primária na AFE.
- Holm: tabela 5 usa a família de 84 testes (assunção; confirmar com o texto do manuscrito).

## Reprodutibilidade

Semente 42 em todos os procedimentos aleatórios (bootstrap, validação cruzada). Versões testadas: Python 3.12+, pandas ≥ 2.1, scipy ≥ 1.11, statsmodels ≥ 0.14, scikit-learn ≥ 1.3.

## Citação e licença

Preencher após aceite (DOI do preprint/artigo). Licença MIT (ver `LICENSE`).
