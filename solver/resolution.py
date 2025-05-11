from typing import List, Tuple, Set
from itertools import combinations

def res_solve(clauses: List[List[int]]) -> Tuple[bool, None]:
    """
    Resolution algorithm for CNF formulas.
    Returns (True, None) if the formula is unsatisfiable (empty clause derived),
    (False, None) otherwise.
    """
    clause_set = {frozenset(clause) for clause in clauses if clause}
    if any(len(c) == 0 for c in clause_set):
        return True, None  # clauză vidă deja prezentă => UNSAT

    MAX_ITER = 10_000
    iteration = 0

    while True:
        iteration += 1
        if iteration > MAX_ITER:
            return False, None  # prea multe iteratii – asumăm SAT (sau timeout extern)

        new_clauses = set()

        for ci, cj in combinations(clause_set, 2):
            resolvents = _resolve(ci, cj)

            if frozenset() in resolvents:
                return True, None  # clauza vidă => UNSAT

            new_clauses.update(resolvents)

        if not new_clauses.difference(clause_set):
            return False, None  # nu am adăugat nimic nou => SAT

        clause_set.update(new_clauses)


def _resolve(clause1: frozenset, clause2: frozenset) -> Set[frozenset]:
    """
    Applies resolution rule between two clauses.
    Returns set of resolvents, excluding tautologies.
    """
    resolvents = set()

    for literal in clause1:
        if -literal in clause2:
            resolvent = (clause1 - {literal}) | (clause2 - {-literal})

            # Tautology check: avoid clauses like [x, ¬x]
            if not any(-lit in resolvent for lit in resolvent):
                resolvents.add(frozenset(resolvent))

    return resolvents
