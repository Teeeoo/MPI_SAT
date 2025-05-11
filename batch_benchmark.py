"""
batch_benchmark.py – rulează benchmark pe grupuri (batch-uri) de fișiere .cnf
pentru a evita blocarea pe instanțe mari (ex. resolution)

Nicio pauză; rulează continuu.

Exemplu:
    python batch_benchmark.py bench --batch-size 5 \
        --solvers dp,res --timeout 60 --csv out.csv
"""

import argparse, csv, sys
from pathlib import Path
from runner import run_once


def parse_args():
    p = argparse.ArgumentParser(description="Batch benchmark SAT solvers on CNF files")
    p.add_argument('folder', help='Folder cu fișiere .cnf (recursiv)')
    p.add_argument('--batch-size', type=int, default=5,
                   help='Număr de fișiere procesate înainte de a continua')
    p.add_argument('--solvers', default='dpll,dp,res',
                   help='Lista solverelor separate prin virgula')
    p.add_argument('--heuristics', default='jw,moms,random,naive',
                   help='Euristici DPLL separate prin virgula')
    p.add_argument('--timeout', type=int, default=60,
                   help='Timeout pe instanță (secunde)')
    p.add_argument('--csv', required=True,
                   help='Fișier CSV pentru rezultate (append)')
    return p.parse_args()


def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i+size]


def main():
    args = parse_args()
    root = Path(args.folder)
    if not root.is_dir():
        sys.exit(f'Folderul {root} nu există')

    files = sorted(root.rglob('*.cnf'))
    if not files:
        sys.exit('Nu există fișiere .cnf în folder')

    solvers = [s.strip() for s in args.solvers.split(',') if s]
    heuristics = [h.strip() for h in args.heuristics.split(',') if h]

    csv_path = Path(args.csv)
    write_header = not csv_path.exists()
    with open(csv_path, 'a', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=['file','solver','heuristic','sat','time','mem_mib'])
        if write_header:
            writer.writeheader()

        for batch_idx, batch in enumerate(chunked(files, args.batch_size)):
            for f in batch:
                for solver in solvers:
                    if solver == 'dpll':
                        for h in heuristics:
                            row = run_once(f, solver, heuristic=h,
                                           pure_literals=True, timeout_sec=args.timeout)
                            row['sat'] = 'SAT' if row['sat'] else 'UNSAT'
                            writer.writerow(row)
                            print(f"{f.name} {solver}/{h}: {row['sat']} {row['time']}s {row['mem_mib']}MiB")
                    else:
                        row = run_once(f, solver, timeout_sec=args.timeout)
                        row['sat'] = 'SAT' if row['sat'] else 'UNSAT'
                        row['heuristic'] = ''
                        writer.writerow(row)
                        print(f"{f.name} {solver}: {row['sat']} {row['time']}s {row['mem_mib']}MiB")

if __name__ == '__main__':
    main()
