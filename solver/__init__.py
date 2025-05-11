from .dp import dp_solve  # Davis–Putnam
from .dpll import dpll_solve  # DPLL + heuristics
from .resolution import res_solve  # Resolutie

__all__ = [
    "dp_solve",
    "dpll_solve",
    "res_solve",
]
__version__ = "0.1.0"