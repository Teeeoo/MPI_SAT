import argparse
from solver.utils import read_cnf_file
from solver.dp import dp_solver
from solver.dpll import dpll
from solver.resolution import resolution_solver

def main():
    parser = argparse.ArgumentParser(description="SAT solver CLI")
    parser.add_argument("--solver", choices=["dp", "dpll", "res"], required=True, help="Tipul de algoritm: dp, dpll, res")
    parser.add_argument("--file", required=True, help="Fișierul .cnf (format DIMACS)")

    args = parser.parse_args()
    num_vars, _, clauses = read_cnf_file(args.file)
    variables = list(range(1, num_vars + 1))

    if args.solver == "dp":
        result = dp_solver(clauses, variables)
    elif args.solver == "dpll":
        result = dpll(clauses)
    elif args.solver == "res":
        result = resolution_solver(clauses)
    else:
        print("solver necunoscut.")
        return

    print("SATISFIABIL" if result else "NESATISFIABIL")

if __name__ == "__main__":
    main()
