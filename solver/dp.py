from copy import deepcopy
from solver.utils import read_cnf_file

def is_pure_literal(literal, clauses):
    """Verifică dacă un literal este pur (apare doar cu un semn)."""
    appears_positive = any(literal in clause for clause in clauses)
    appears_negative = any(-literal in clause for clause in clauses)
    return appears_positive != appears_negative

def eliminate_pure_literals(clauses):
    """Elimină clauze care conțin literali puri."""
    all_literals = set(l for clause in clauses for l in clause)
    pure_literals = [l for l in all_literals if is_pure_literal(l, clauses)]

    new_clauses = [clause for clause in clauses if not any(l in clause for l in pure_literals)]
    return new_clauses

def resolve_clauses(cl1, cl2, var):
    """Rezolvă două clauze care conțin var și -var."""
    return list(set([l for l in cl1 + cl2 if l != var and l != -var]))

def dp_solver(clauses, variables):
    """Algoritmul Davis–Putnam (fără literali puri, opțional)."""
    clauses = eliminate_pure_literals(clauses)

    if not clauses:
        return True  # formula este satisfiabilă
    if [] in clauses:
        return False  # clauza vidă → nesatisfiabilă

    # Alege prima variabilă
    for var in variables:
        break

    # Clauze cu var și -var
    pos_clauses = [c for c in clauses if var in c]
    neg_clauses = [c for c in clauses if -var in c]
    other_clauses = [c for c in clauses if var not in c and -var not in c]

    # Generează toate rezolventele
    resolvents = [resolve_clauses(p, n, var) for p in pos_clauses for n in neg_clauses]

    new_clauses = other_clauses + resolvents
    new_variables = [v for v in variables if v != var]

    return dp_solver(new_clauses, new_variables)

# Pentru test
if __name__ == "__main__":
    num_vars, _, clauses = read_cnf_file("test.cnf")
    variables = list(range(1, num_vars + 1))
    result = dp_solver(clauses, variables)
    print("SATISFIABIL" if result else "NESATISFIABIL")
