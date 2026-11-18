# NÃO EXECUTADO NO AMBIENTE DE AUDITORIA (R indisponível). Rodar localmente e conferir contra as Tabelas 1 e 4.
# Requer: psych, GPArotation. Entrada: data/processed/less_items_recodificados.csv (python scripts/06_export_for_r.py)
suppressPackageStartupMessages({library(psych); library(GPArotation)})
set.seed(42)
x <- read.csv2("data/processed/less_items_recodificados.csv")
dir.create("outputs/r", showWarnings = FALSE, recursive = TRUE)

poly <- polychoric(x)$rho                     # matriz policórica 28 x 28
ev <- eigen(poly)$values
write.csv(data.frame(componente = seq_along(ev), autovalor = ev), "outputs/r/autovalores_policoricos.csv", row.names = FALSE)
cat("lambda1/lambda2 =", ev[1] / ev[2], "\n")

# Análise paralela (variantes) — registrar TODAS no manuscrito
pa_pc  <- fa.parallel(poly, n.obs = nrow(x), fa = "pc", n.iter = 500, plot = FALSE)
pa_fa  <- fa.parallel(poly, n.obs = nrow(x), fa = "fa", fm = "minres", n.iter = 500, plot = FALSE)
cat("PA (componentes):", pa_pc$ncomp, " PA (eixos principais):", pa_fa$nfact, "\n")

# AFE (resíduo mínimo, oblimin), 1 a 5 fatores
for (k in 1:5) {
  f <- fa(poly, nfactors = k, n.obs = nrow(x), fm = "minres", rotate = "oblimin")
  write.csv(unclass(f$loadings), sprintf("outputs/r/afe_%dfatores_cargas.csv", k))
}

# Fidedignidade: alfa ordinal do total e das 14 subescalas (correlação policórica)
alpha_ord <- function(R) { k <- ncol(R); rbar <- (sum(R) - k) / (k * (k - 1)); k * rbar / (1 + (k - 1) * rbar) }
cat("alfa ordinal (28 itens):", alpha_ord(poly), "\n")
