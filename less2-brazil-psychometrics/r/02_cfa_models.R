# NÃO EXECUTADO NO AMBIENTE DE AUDITORIA (R indisponível). Rodar localmente; conferir Tabela 2 e exportar cargas para o Python.
# Requer: lavaan >= 0.6-17. Entrada: data/processed/less_items_recodificados.csv
suppressPackageStartupMessages(library(lavaan))
x <- read.csv2("data/processed/less_items_recodificados.csv")
nm <- names(x); stopifnot(length(nm) == 28)
dir.create("outputs/r", showWarnings = FALSE, recursive = TRUE)
mk <- function(f) paste(names(f), "=~", sapply(f, function(i) paste(sprintf("less_%d", i), collapse = " + ")), collapse = "\n")

F5  <- list(F1 = c(3,5,7,9,10,16,17,20,22), F2 = c(14,21,23,26,28), F3 = c(11,13,27), F4 = c(2,18,19), F5 = c(1,4,6,8,12,15,24,25))
L14 <- list(Invalid = c(6,12), Incomp = c(3,7), Culpa = c(2,10), Simpl = c(23,28), Desval = c(14,26), Controle = c(5,17), Numb = c(11,20),
            Racion = c(13,27), Duracao = c(9,19), Consenso = c(1,25), NaoAcei = c(18,24), Rumin = c(16,22), Expr = c(4,15), Culpab = c(8,21))
m_uni  <- sprintf("G =~ %s", paste(nm, collapse = " + "))
m_l14  <- mk(L14)
m_f5   <- mk(F5)
m_bif  <- paste(sprintf("G =~ %s", paste(nm, collapse = " + ")), mk(F5), sep = "\n")

fit <- function(model, orth = FALSE)
  cfa(model, data = x, ordered = nm, estimator = "WLSMV", std.lv = TRUE, orthogonal = orth)
fits <- list(uni = fit(m_uni), l14 = fit(m_l14), f5 = fit(m_f5), bif = fit(m_bif, orth = TRUE))

idx <- c("chisq.scaled", "df.scaled", "cfi.scaled", "tli.scaled", "rmsea.scaled", "rmsea.ci.lower.scaled", "rmsea.ci.upper.scaled", "srmr")
tab <- do.call(rbind, lapply(names(fits), function(k) {
  f <- fits[[k]]
  ok <- tryCatch(lavInspect(f, "post.check"), error = function(e) NA)   # admissibilidade (cov. latente PD, variâncias >= 0)
  data.frame(modelo = k, t(round(fitMeasures(f, idx), 3)), admissivel = ok)
}))
write.csv(tab, "outputs/r/tabela2_ajuste.csv", row.names = FALSE)

# Cargas padronizadas do bifatorial -> Python calcula ω, ωH, ECV, PUC, ωHS (scripts/07_...)
pe <- standardizedSolution(fits$bif); pe <- pe[pe$op == "=~", ]
pe$item <- as.integer(sub("less_", "", pe$rhs))
lg <- pe[pe$lhs == "G", c("item", "est.std")]; names(lg)[2] <- "lambda_G"
ls_ <- pe[pe$lhs != "G", c("item", "est.std")]; names(ls_)[2] <- "lambda_S"
write.csv(merge(lg, ls_, by = "item"), "outputs/r/bifactor_loadings.csv", row.names = FALSE)

# Para o modelo de 14 fatores: relatar a faixa das correlações latentes (defeito 11 da auditoria)
cl <- lavInspect(fits$l14, "cor.lv"); cat("faixa cor.lv:", range(cl[lower.tri(cl)]), "\n")
