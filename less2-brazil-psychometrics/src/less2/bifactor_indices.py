"""Índices de modelos bifatoriais a partir de cargas PADRONIZADAS (Rodriguez, Reise & Haviland, 2016).
Itens contínuos/ordinais tratados como na saída do lavaan (WLSMV): variância residual = 1 - lG^2 - lS^2."""
from itertools import combinations
import numpy as np


def bifactor_indices(lg, ls, groups):
    """lg: cargas no fator geral (n,); ls: cargas no fator específico do próprio item (n,);
    groups: dict {nome_fator: [índices 0-based dos itens]}. Retorna ω, ωH, ECV, PUC, ωHS por fator."""
    lg = np.asarray(lg, float); ls = np.asarray(ls, float); n = len(lg)
    resid = 1 - lg ** 2 - ls ** 2
    num_g = lg.sum() ** 2
    spec = {k: ls[idx].sum() ** 2 for k, idx in groups.items()}
    var_tot = num_g + sum(spec.values()) + resid.sum()
    omega = (num_g + sum(spec.values())) / var_tot
    omega_h = num_g / var_tot
    ecv = (lg ** 2).sum() / ((lg ** 2).sum() + (ls ** 2).sum())
    total_pairs = n * (n - 1) / 2
    within = sum(len(list(combinations(idx, 2))) for idx in groups.values())
    puc = (total_pairs - within) / total_pairs
    omega_hs = {}
    for k, idx in groups.items():
        v = lg[idx].sum() ** 2 + ls[idx].sum() ** 2 + resid[idx].sum()
        omega_hs[k] = spec[k] / v
    return dict(omega=omega, omega_h=omega_h, omega_h_sobre_omega=omega_h / omega, ecv=ecv, puc=puc, omega_hs=omega_hs)
