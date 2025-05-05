from copy import deepcopy
from solver.utils import read_cnf_file

def unit_propagate(clauses, assignment):
    changed = True
    while changed:
        changed = False
        unit_clauses = [c for c in clauses if len(c) == 1]
        for unit in unit_clauses:
            literal = unit[0]
            assignment.add(literal)
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue  # clauza devine adevărată
                new_clause = [l for l in clause if l != -literal]
                if len(new_clause) == 0:
                    return None, None  # conflict
                new_clauses.append(new_clause)
            clauses = new_clauses
            changed = True
    return clauses, assignment

def pure_literal_elimination(clauses, assignment):
    all_literals = set(l for clause in clauses for l in clause)
    for lit in all_literals:
        if -lit not in all_literals:
            assignment.add(lit)
            clauses = [c for c in clauses if lit not in c]
    return clauses, assignment

def dpll(clauses, assignment=set()):
    clauses, assignment = unit_propagate(clauses, assignment)
    if clauses is None:
        return False

    if not clauses:
        return True

    clauses, assignment = pure_literal_elimination(clauses, assignment)
    if not clauses:
        return True

    # Alegem prima variabilă
    for clause in clauses:
        for literal in clause:
            var = abs(literal)
            break
        break

    for guess in [var, -var]:
        new_clauses = deepcopy(clauses)
        new_assignment = assignment.copy()
        new_clauses.append([guess])
        result = dpll(new_clauses, new_assignment)
        if result:
            return True
    return False

# Test simplu
if __name__ == "__main__":
    num_vars, _, clauses = read_cnf_file("test.cnf")
    result = dpll(clauses)
    print("SATISFIABIL" if result else "NESATISFIABIL")
