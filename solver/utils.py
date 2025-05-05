def read_cnf_file(filename):
    """
    Citește un fișier .cnf în format DIMACS și returnează:
    - numărul de variabile
    - numărul de clauze
    - lista de clauze (fiecare clauză e o listă de litere întregi)
    """
    clauses = []
    num_vars = num_clauses = 0

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == '' or line.startswith('c'):
                continue
            if line.startswith('p'):
                parts = line.split()
                num_vars = int(parts[2])
                num_clauses = int(parts[3])
            else:
                literals = list(map(int, line.split()))
                if literals[-1] == 0:
                    literals = literals[:-1]
                clauses.append(literals)

    return num_vars, num_clauses, clauses