"""
benchmark.py – rulează automat solvere SAT pe un set de fișiere .cnf
și colectează metrice (timp, memorie, rezultat) într-un CSV.

Implicit: DPLL cu toate cele patru euristici (`jw,moms,random,naive`)
plus DP și Rezoluție o singură dată.
"""

from pathlib import Path
import argparse, csv, sys
from runner import run_once

# ------------------
# Argumente CLI
# ------------------

def parse_args():
    p = argparse.ArgumentParser(description="Benchmark SAT solvers on a folder of CNF files")
    p.add_argument("folder", help="Director cu fișiere .cnf (recursiv)")
    p.add_argument("--solvers", default="dpll,dp,res",
                   help="Lista solverelor: dp,dpll,res (implicit toate)")
    p.add_argument("--heuristics", default="jw,moms,random,naive",
                   help="Euristici pentru DPLL (implicit toate patru)")
    p.add_argument("--timeout", type=int, default=60,
                   help="Timeout pe instanță (sec). 0 = fără limită")
    p.add_argument("--csv", help="Fișier CSV pentru rezultate (append)")
    return p.parse_args()

# ------------------
# Main
# ------------------

def main():
    args = parse_args()
    root = Path(args.folder)
    if not root.is_dir():
        sys.exit(f"Folderul {root} nu există")

    solvers = [s for s in args.solvers.split(',') if s]
    heuristics = [h for h in args.heuristics.split(',') if h]

    files = sorted(root.rglob("*.cnf"))
    if not files:
        sys.exit("Nu există fișiere .cnf în folderul specificat.")

    rows = []
    for f in files:
        for s in solvers:
            if s == "dpll":
                for h in heuristics:
                    row = run_once(f, s, heuristic=h,
                                   pure_literals=True,
                                   timeout_sec=args.timeout)
                    row["sat"] = "SAT" if row["sat"] else "UNSAT"
                    rows.append(row)
            else:
                row = run_once(f, s, timeout_sec=args.timeout)
                row["sat"] = "SAT" if row["sat"] else "UNSAT"
                rows.append(row)

    # afișează rezumat
    for r in rows:
        print(f"{r['file']:<25} {r['solver']:^5} {r['heuristic']:^6} "
              f"{r['sat']:^8} {r['time']:>6}s {r['mem_mib']:>6} MiB")

    # scrie CSV dacă s-a cerut
    if args.csv:
        csv_path = Path(args.csv)
        write_header = not csv_path.exists()
        with open(csv_path, "a", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=rows[0].keys())
            if write_header:
                w.writeheader()
            w.writerows(rows)
        print(f"Written {len(rows)} rows to {csv_path}")

if __name__ == "__main__":
    main()
