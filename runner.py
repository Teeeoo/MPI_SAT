# runner.py – with timeout support via multiprocessing
import argparse, importlib, time, tracemalloc, multiprocessing
from pathlib import Path
from typing import Tuple, List, Dict

# ------------------------------
# Helper: cititor DIMACS CNF
# ------------------------------
def read_cnf_file(path: str) -> Tuple[int, int, List[List[int]]]:
    clauses: List[List[int]] = []
    n_vars = n_clauses = 0
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith(("c", "%")):
                continue
            if line.startswith("p"):
                _, _, n_vars, n_clauses = line.split()[:4]
                n_vars, n_clauses = int(n_vars), int(n_clauses)
            else:
                lits = []
                for tok in line.split():
                    if tok == "0":
                        break
                    try:
                        lits.append(int(tok))
                    except ValueError:
                        break
                if lits:
                    clauses.append(lits)
    return n_vars, n_clauses, clauses

# -------------------------------------------------
# Mapping solver keys -> (module_name, function_name)
# -------------------------------------------------
SOLVERS = {
    "dp":   ("solver.dp",         "dp_solve"),
    "dpll": ("solver.dpll",       "dpll_solve"),
    "res":  ("solver.resolution", "res_solve"),
}

def load_solver(key: str):
    mod, fn = SOLVERS[key]
    return getattr(importlib.import_module(mod), fn)

# -------------------------------------------------
# run_once – helper folosit de benchmark.py
# with timeout support
# -------------------------------------------------

def _worker(clauses, solver_key, heuristic, pure_literals, return_dict):
    solve = load_solver(solver_key)
    if solver_key == "dpll":
        sat, _ = solve(clauses, heuristic=heuristic, pure_literals=pure_literals)
    else:
        sat, _ = solve(clauses)
    return_dict['sat'] = sat


def run_once(
    cnf_path: Path,
    solver_key: str,
    heuristic: str = "jw",
    pure_literals: bool = True,
    timeout_sec: int = 0,
) -> Dict:
    _, _, clauses = read_cnf_file(str(cnf_path))

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    return_dict['sat'] = None

    # start measurement
    tracemalloc.start()
    t0 = time.perf_counter()

    p = multiprocessing.Process(
        target=_worker,
        args=(clauses, solver_key, heuristic, pure_literals, return_dict)
    )
    p.start()
    p.join(timeout_sec if timeout_sec > 0 else None)

    if p.is_alive():
        p.terminate()
        sat = False  # treated as UNSAT on timeout
    else:
        sat = return_dict.get('sat', False)

    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "file": cnf_path.name,
        "solver": solver_key,
        "heuristic": heuristic if solver_key == "dpll" else "",
        "sat": sat,
        "time": round(elapsed, 3),
        "mem_mib": round(peak / 1_048_576, 2),
    }

# -------------------------------------------------
# CLI – util pentru rulări punctuale
# -------------------------------------------------
def main():
    p = argparse.ArgumentParser(description="Run a SAT solver on a DIMACS CNF file.")
    p.add_argument("cnf", help="Path to .cnf file (DIMACS)")
    p.add_argument("--solver", choices=SOLVERS, default="dpll")
    p.add_argument("--heuristic", default="jw")
    p.add_argument("--pure-literals", action="store_true")
    p.add_argument("--timeout", type=int, default=0,
                   help="Timeout on each instance (seconds)")
    args = p.parse_args()

    if not Path(args.cnf).is_file():
        p.error("CNF file not found: " + args.cnf)

    row = run_once(Path(args.cnf), args.solver,
                   args.heuristic, args.pure_literals, args.timeout)
    status = 'SAT' if row['sat'] else 'UNSAT'
    print(f"{status}  |  {row['time']:.3f}s  |  {row['mem_mib']:.1f} MiB")

if __name__ == "__main__":
    main()
