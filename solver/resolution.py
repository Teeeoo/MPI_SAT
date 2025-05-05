from solver.utils import read_cnf_file
from itertools import combinations

def resolve(clause1, clause2):
    resolvents = []
    for literal in clause1:
        if -literal in clause2:
            new_clause = set(clause1 + clause2)
            new_clause.discard(literal)
            new_clause.discard(-literal)
            resolvents.append(list(new_clause))
    return resolvents

def resolution_solver(clauses):
    clauses = [set(c) for c in clauses]  # set pentru eliminare rapidă
    new = set()

    while True:
        n = len(clauses)
        pairs = combinations(clauses, 2)
        for (ci, cj) in pairs:
            resolvents = resolve(list(ci), list(cj))
            for r in resolvents:
                if len(r) == 0:
                    return False  # clauză vidă = nesatisfiabil
                new_clause = frozenset(r)
                if new_clause not in clauses:
                    new.add(new_clause)
        if new.issubset(set(map(frozenset, clauses))):
            return True  # nimic nou, nu s-a obținut clauza vidă
        for c in new:
            if c not in clauses:
                clauses.append(set(c))

# Test simplu
if __name__ == "__main__":
    num_vars, _, clauses = read_cnf_file("test.cnf")
    result = resolution_solver(clauses)
    print("SATISFIABIL" if result else "NESATISFIABIL")
