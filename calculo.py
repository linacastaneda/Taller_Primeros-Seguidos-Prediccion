# ============================================================
# CALCULO GENERAL DE PRIMEROS, SIGUIENTES Y PREDICCION
# PARA GRAMATICAS LIBRES DE CONTEXTO
#
# Formato esperado de la gramática:
#   S -> A uno B C | S dos
#   A -> B C D | A tres | ε
#   B -> D cuatro C tres | ε
#   C -> cinco D B | ε
#   D -> seis | ε
#
# Notas:
# - No terminales: símbolos del lado izquierdo de alguna regla
# - Terminales: símbolos que NO están en los lados izquierdos
# - ε representa epsilon
# - No se modifica la gramática, solo se calculan conjuntos
# ============================================================

EPSILON = "ε"
ENDMARK = "$"


# ------------------------------------------------------------
# PARSEO DE LA GRAMATICA DESDE TEXTO
# ------------------------------------------------------------
def parse_grammar(grammar_text):
    """
    Convierte una gramática en texto a un diccionario:
    {
        "S": [["A", "uno", "B", "C"], ["S", "dos"]],
        ...
    }
    """
    grammar = {}

    lines = grammar_text.strip().splitlines()
    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        if "->" not in line:
            raise ValueError(f"Línea inválida (falta '->'): {line}")

        left, right = line.split("->", 1)
        left = left.strip()
        right = right.strip()

        alternatives = [alt.strip() for alt in right.split("|")]
        productions = []

        for alt in alternatives:
            if alt == "":
                raise ValueError(f"Producción vacía inválida en línea: {line}")

            symbols = alt.split()
            productions.append(symbols)

        if left not in grammar:
            grammar[left] = []

        grammar[left].extend(productions)

    return grammar


# ------------------------------------------------------------
# UTILIDADES
# ------------------------------------------------------------
def get_non_terminals(grammar):
    return set(grammar.keys())


def get_terminals(grammar, non_terminals):
    terminals = set()
    for left, productions in grammar.items():
        for prod in productions:
            for sym in prod:
                if sym not in non_terminals and sym != EPSILON:
                    terminals.add(sym)
    return terminals


def is_non_terminal(symbol, non_terminals):
    return symbol in non_terminals


def is_terminal(symbol, non_terminals):
    return symbol not in non_terminals and symbol != EPSILON


# ------------------------------------------------------------
# PRIMEROS DE UNA SECUENCIA
# FIRST(α)
# ------------------------------------------------------------
def first_of_sequence(sequence, first_sets, non_terminals):
    """
    Calcula PRIMEROS de una secuencia α = X1 X2 ... Xn
    """
    if not sequence:
        return {EPSILON}

    if sequence == [EPSILON]:
        return {EPSILON}

    result = set()
    all_nullable = True

    for symbol in sequence:
        if symbol == EPSILON:
            result.add(EPSILON)
            return result

        if is_terminal(symbol, non_terminals):
            result.add(symbol)
            all_nullable = False
            break

        if is_non_terminal(symbol, non_terminals):
            result |= (first_sets[symbol] - {EPSILON})

            if EPSILON in first_sets[symbol]:
                continue
            else:
                all_nullable = False
                break

    if all_nullable:
        result.add(EPSILON)

    return result


# ------------------------------------------------------------
# CALCULO DE PRIMEROS
# ------------------------------------------------------------
def compute_first_sets(grammar):
    non_terminals = get_non_terminals(grammar)
    first_sets = {nt: set() for nt in non_terminals}

    changed = True
    while changed:
        changed = False

        for left, productions in grammar.items():
            for prod in productions:
                before = len(first_sets[left])

                seq_first = first_of_sequence(prod, first_sets, non_terminals)
                first_sets[left] |= seq_first

                if len(first_sets[left]) > before:
                    changed = True

    return first_sets


# ------------------------------------------------------------
# CALCULO DE SIGUIENTES
# ------------------------------------------------------------
def compute_follow_sets(grammar, first_sets, start_symbol):
    non_terminals = get_non_terminals(grammar)
    follow_sets = {nt: set() for nt in non_terminals}
    follow_sets[start_symbol].add(ENDMARK)

    changed = True
    while changed:
        changed = False

        for left, productions in grammar.items():
            for prod in productions:
                for i, symbol in enumerate(prod):
                    if not is_non_terminal(symbol, non_terminals):
                        continue

                    beta = prod[i + 1:]
                    first_beta = first_of_sequence(beta, first_sets, non_terminals)

                    before = len(follow_sets[symbol])

                    # FIRST(beta) - {ε}
                    follow_sets[symbol] |= (first_beta - {EPSILON})

                    # Si beta =>* ε o beta es vacía, agregar FOLLOW(left)
                    if not beta or EPSILON in first_beta:
                        follow_sets[symbol] |= follow_sets[left]

                    if len(follow_sets[symbol]) > before:
                        changed = True

    return follow_sets


# ------------------------------------------------------------
# CALCULO DE PREDICCION
# ------------------------------------------------------------
def compute_prediction_sets(grammar, first_sets, follow_sets):
    non_terminals = get_non_terminals(grammar)
    prediction_sets = []

    for left, productions in grammar.items():
        for idx, prod in enumerate(productions, start=1):
            first_alpha = first_of_sequence(prod, first_sets, non_terminals)

            if EPSILON in first_alpha:
                pred = (first_alpha - {EPSILON}) | follow_sets[left]
            else:
                pred = set(first_alpha)

            prediction_sets.append({
                "left": left,
                "index": idx,
                "production": prod,
                "prediction": pred
            })

    return prediction_sets


# ------------------------------------------------------------
# OPCIONAL: DETECTAR CONFLICTOS LL(1)
# ------------------------------------------------------------
def detect_ll1_conflicts(grammar, prediction_sets):
    """
    Revisa si para un mismo no terminal hay intersección
    entre conjuntos de predicción de distintas reglas.
    """
    grouped = {}

    for item in prediction_sets:
        left = item["left"]
        grouped.setdefault(left, []).append(item)

    conflicts = []

    for left, rules in grouped.items():
        for i in range(len(rules)):
            for j in range(i + 1, len(rules)):
                inter = rules[i]["prediction"] & rules[j]["prediction"]
                if inter:
                    conflicts.append({
                        "non_terminal": left,
                        "rule1": rules[i],
                        "rule2": rules[j],
                        "intersection": inter
                    })

    return conflicts


# ------------------------------------------------------------
# FORMATO DE IMPRESION
# ------------------------------------------------------------
def sort_symbols(symbols):
    preferred = ["uno", "dos", "tres", "cuatro", "cinco", "seis", ENDMARK, EPSILON]
    ordered = [s for s in preferred if s in symbols]
    remaining = sorted(s for s in symbols if s not in preferred)
    return remaining + ordered


def format_set(symbols):
    return "{ " + ", ".join(sort_symbols(symbols)) + " }"


def prod_to_string(left, production):
    return f"{left} -> {' '.join(production)}"


def print_results(grammar, first_sets, follow_sets, prediction_sets):
    print("=" * 70)
    print("GRAMATICA")
    print("=" * 70)
    for left, productions in grammar.items():
        for prod in productions:
            print(prod_to_string(left, prod))

    print("\n" + "=" * 70)
    print("PRIMEROS")
    print("=" * 70)
    for nt in sorted(grammar.keys()):
        print(f"PRIMEROS({nt}) = {format_set(first_sets[nt])}")

    print("\n" + "=" * 70)
    print("SIGUIENTES")
    print("=" * 70)
    for nt in sorted(grammar.keys()):
        print(f"SIGUIENTES({nt}) = {format_set(follow_sets[nt])}")

    print("\n" + "=" * 70)
    print("PREDICCION")
    print("=" * 70)
    for item in prediction_sets:
        print(
            f"PRED({prod_to_string(item['left'], item['production'])}) = "
            f"{format_set(item['prediction'])}"
        )


# ------------------------------------------------------------
# FUNCION PRINCIPAL GENERAL
# ------------------------------------------------------------
def analyze_grammar(grammar_text, start_symbol):
    grammar = parse_grammar(grammar_text)
    first_sets = compute_first_sets(grammar)
    follow_sets = compute_follow_sets(grammar, first_sets, start_symbol)
    prediction_sets = compute_prediction_sets(grammar, first_sets, follow_sets)

    print_results(grammar, first_sets, follow_sets, prediction_sets)

    conflicts = detect_ll1_conflicts(grammar, prediction_sets)

    print("\n" + "=" * 70)
    print("REVISION DE CONFLICTOS DE PREDICCION")
    print("=" * 70)
    if not conflicts:
        print("No se detectaron conflictos entre conjuntos de predicción.")
    else:
        print("Se detectaron conflictos:")
        for c in conflicts:
            r1 = prod_to_string(c["rule1"]["left"], c["rule1"]["production"])
            r2 = prod_to_string(c["rule2"]["left"], c["rule2"]["production"])
            print(f"\nNo terminal: {c['non_terminal']}")
            print(f"  Regla 1: {r1}")
            print(f"  Regla 2: {r2}")
            print(f"  Intersección: {format_set(c['intersection'])}")


# ------------------------------------------------------------
# EJEMPLO DE USO: PRIMER EJERCICIO, PRIMERA GRAMATICA
# ------------------------------------------------------------
if __name__ == "__main__":
    grammar_text = """
    S -> A uno B C | S dos
    A -> B C D | A tres | ε
    B -> D cuatro C tres | ε
    C -> cinco D B | ε
    D -> seis | ε
    """

    analyze_grammar(grammar_text, start_symbol="S")