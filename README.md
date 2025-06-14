
# SAT Solvers (Davis–Putnam, DPLL și Rezoluție)

Acest proiect conține trei algoritmi clasici pentru verificarea satisfiabilității (SAT):

- **dp.py** – Davis–Putnam (eliminarea variabilelor)
- **dpll.py** – DPLL cu propagare unitară, eliminare literal pur și euristici configurabile
- **resolution.py** – procedura de rezoluție în formă clauzală

## Structura directorului

```
solver/
├── dp.py          # Davis–Putnam
├── dpll.py        # DPLL + euristici (jw, moms, random, naive)
├── resolution.py  # Rezoluție
└── __init__.py    # API public (dp_solve, dpll_solve, res_solve)
batch_benchmark.py # Rulare automată pe batch-uri de fișiere CNF
benchmark.py       # Rulare automată de fișiere CNF
runner.py          # Script CLI de test
README.md          # Acest fișier
```

## Instalare

Proiectul funcționează cu **Python ≥ 3.8** și nu are dependențe externe.

```bash
git clone <repo_url> MPI_SAT
cd MPI_SAT
pip install -e .  # Opțional, pentru rulare globală
```

## Utilizare din linia de comandă

### 1. Rulare simplă
```bash
python runner.py <fisier>.cnf --solver dpll --heuristic jw
python runner.py <fisier>.cnf --solver dp
python runner.py <fisier>.cnf --solver res
```

### 2. Batch Benchmark
```bash
python batch_benchmark.py bench --batch-size 5 --solvers dp,res,dpll --timeout 60 --csv results.csv
```

## Parametri

- `--solver`: `dpll` (implicit) | `dp` | `res`
- `--heuristic`: `jw`, `moms`, `random`, `naive` (doar pentru `dpll`)
- `--pure-literals`: activează eliminarea literalilor puri în DPLL

### Euristici disponibile pentru `dpll_solve`

| Nume          | Parametru | Descriere                             |
|---------------|-----------|---------------------------------------|
| Naive         | `naive`   | Primul literal din prima clauză       |
| Random        | `random`  | Alege literal aleatoriu               |
| Jeroslow–Wang | `jw`      | Scor ponderat 2^(-dimensiune clauză)  |
| MOMS          | `moms`    | Maximizează aparițiile în clauze mici |
## Exemplu de rulare
```bash
python runner.py bench/uf50-218.cnf --solver dpll --heuristic jw
# Output: SAT | 0.152s | 11.4 MiB
```

## Despre `batch_benchmark.py`

Scriptul `batch_benchmark.py` rulează automat benchmark-uri pe loturi (batch-uri) de fișiere `.cnf`, evitând blocajele pe instanțele mari. Ideal pentru testare masivă și generare fișier CSV.
