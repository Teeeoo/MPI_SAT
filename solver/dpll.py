"""
dpll.py - Solver DPLL clasic cu backtracking si euristici
"""

import random
from collections import Counter
import sys

sys.setrecursionlimit(10_000)

# -------------------------------------------------
# Functii auxiliare
# -------------------------------------------------

def _unit_propagate(clauses, assignment):
    """Propagare unitara; intoarce clauze reduse sau None la conflict."""
    changed = True
    while changed:
        changed = False
        for c in clauses:
            if len(c) == 1:
                lit = c[0]
                var, val = abs(lit), lit > 0
                if var in assignment and assignment[var] != val:
                    return None  # conflict
                if var not in assignment:
                    assignment[var] = val
                    changed = True
                # Simplificare formula curenta
                new_clauses = []
                for cl in clauses:
                    if lit in cl:
                        continue  # clauza satisfacuta
                    new_clause = [l for l in cl if l != -lit]
                    if not new_clause:
                        return None  # clauza vida -> conflict
                    new_clauses.append(new_clause)
                clauses = new_clauses
                break
    return clauses


def _pure_literal_elim(clauses, assignment):
    """Elimina literalii puri si inregistreaza valorile lor."""
    literals = {l for c in clauses for l in c}
    pures = [l for l in literals if -l not in literals]
    if not pures:
        return clauses
    for lit in pures:
        assignment[abs(lit)] = lit > 0
    return [c for c in clauses if not any(l in c for l in pures)]


def _choose_literal(clauses, heuristic):
    """Alege un literal dupa euristica specificata."""
    if heuristic == "random":
        return random.choice(random.choice(clauses))
    if heuristic == "jw":
        score = Counter()
        for c in clauses:
            weight = 2 ** (-len(c))
            for lit in c:
                score[lit] += weight
        return max(score, key=score.get)
    if heuristic == "moms":
        min_len = min(len(c) for c in clauses)
        min_c = [c for c in clauses if len(c) == min_len]
        occ = Counter(l for c in min_c for l in c)
        return max(occ, key=occ.get)
    # fallback naive
    return clauses[0][0]


# -------------------------------------------------
# Recursie principala
# -------------------------------------------------

def _dpll(clauses, assignment, heuristic, pure_literals):
    clauses = _unit_propagate(clauses, assignment)
    if clauses is None:
        return False
    if not clauses:
        return True  # satisfiabil
    if pure_literals:
        clauses = _pure_literal_elim(clauses, assignment)
        if not clauses:
            return True

    lit = _choose_literal(clauses, heuristic)
    var = abs(lit)

    for guess in (lit, -lit):
        assignment_copy = assignment.copy()
        assignment_copy[var] = guess > 0
        new_clauses = [cl[:] for cl in clauses] + [[guess]]
        if _dpll(new_clauses, assignment_copy, heuristic, pure_literals):
            assignment.update(assignment_copy)
            return True
    return False


def dpll_solve(clauses, heuristic="jw", pure_literals=True):
    """
    Punct de intrare pentru DPLL.

    Parametri:
        clauses : lista de clauze (iterabile de int).
        heuristic : 'naive', 'random', 'jw' sau 'moms'.
        pure_literals : activeaza eliminarea literali puri.

    Returneaza:
        sat (bool) si model (dict var->valoare) daca sat este True.
    """
    clauses = [list(c) for c in clauses]
    assignment = {}
    sat = _dpll(clauses, assignment, heuristic, pure_literals)
    return sat, assignment if sat else None
