

EPSILON = "ε"
ENDMARK = "$"


# PARSEO DE LA GRAMÁTICA
# Formato esperado:
#   S -> A uno B C | S dos
#   A -> B C D | A tres | ε
def analizar_gramatica(grammar_text):
    """
    Parsea el texto de la gramática en un diccionario.

    Args:
        grammar_text (str): Texto de la gramática en formato específico.

    Returns:
        dict: Diccionario con no terminales como claves y listas de producciones como valores.

    Raises:
        ValueError: Si hay líneas inválidas o producciones vacías.
    """
    grammar = {}

    lines = grammar_text.strip().splitlines()
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        if "->" not in line:
            raise ValueError(f"Línea inválida: {line}")

        left, right = line.split("->", 1)
        left = left.strip()
        right = right.strip()

        alternatives = [alt.strip() for alt in right.split("|")]

        productions = []
        for alt in alternatives:
            if not alt:
                raise ValueError(f"Producción inválida en línea: {line}")
            productions.append(alt.split())

        grammar.setdefault(left, []).extend(productions)

    return grammar


# UTILIDADES BÁSICAS
def obtener_no_terminales(grammar):
    """
    Obtiene el conjunto de no terminales de la gramática.
    """
    return set(grammar.keys())


def es_no_terminal(symbol, non_terminals):
    """
    Verifica si un símbolo es un no terminal.
    """
    return symbol in non_terminals


def es_terminal(symbol, non_terminals):
    """
    Verifica si un símbolo es un terminal.
    """
    return symbol not in non_terminals and symbol != EPSILON


def produccion_a_cadena(left, prod):
    """
    Convierte una producción a string.
    """
    return f"{left} → {' '.join(prod)}"


def formatear_conjunto(symbols):
    """
    Formatea un conjunto de símbolos como string.
    """
    ordered = sorted(symbols)
    return "{ " + ", ".join(ordered) + " }"


# PRIMEROS DE UNA SECUENCIA
def primeros_de_secuencia(sequence, first_sets, non_terminals):
    """
    Calcula el conjunto FIRST de una secuencia de símbolos.
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

        if es_terminal(symbol, non_terminals):
            result.add(symbol)
            all_nullable = False
            break

        if es_no_terminal(symbol, non_terminals):
            result |= (first_sets[symbol] - {EPSILON})

            if EPSILON in first_sets[symbol]:
                continue

            all_nullable = False
            break

    if all_nullable:
        result.add(EPSILON)

    return result


# CÁLCULO DE PRIMEROS
def calcular_primeros(grammar):
    """
    Calcula los conjuntos FIRST para todos los no terminales.
    """
    non_terminals = obtener_no_terminales(grammar)
    first_sets = {nt: set() for nt in non_terminals}

    changed = True
    while changed:
        changed = False

        for left, productions in grammar.items():
            for prod in productions:
                before = len(first_sets[left])
                first_sets[left] |= primeros_de_secuencia(prod, first_sets, non_terminals)
                if len(first_sets[left]) > before:
                    changed = True

    return first_sets


# CÁLCULO DE SIGUIENTES
def calcular_siguientes(grammar, first_sets, start_symbol):
    """
    Calcula los conjuntos FOLLOW para todos los no terminales.
    """
    non_terminals = obtener_no_terminales(grammar)
    follow_sets = {nt: set() for nt in non_terminals}
    follow_sets[start_symbol].add(ENDMARK)

    changed = True
    while changed:
        changed = False

        for left, productions in grammar.items():
            for prod in productions:
                for i, symbol in enumerate(prod):
                    if not es_no_terminal(symbol, non_terminals):
                        continue

                    beta = prod[i + 1:]
                    first_beta = primeros_de_secuencia(beta, first_sets, non_terminals)

                    before = len(follow_sets[symbol])

                    follow_sets[symbol] |= (first_beta - {EPSILON})

                    if not beta or EPSILON in first_beta:
                        follow_sets[symbol] |= follow_sets[left]

                    if len(follow_sets[symbol]) > before:
                        changed = True

    return follow_sets


# CÁLCULO DE PREDICCIÓN
def calcular_prediccion(grammar, first_sets, follow_sets):
    """
    Calcula los conjuntos de predicción para cada producción.
    """
    non_terminals = obtener_no_terminales(grammar)
    prediction_sets = []

    for left, productions in grammar.items():
        for idx, prod in enumerate(productions, start=1):
            first_alpha = primeros_de_secuencia(prod, first_sets, non_terminals)

            if EPSILON in first_alpha:
                prediction = (first_alpha - {EPSILON}) | follow_sets[left]
                uses_follow = True
            else:
                prediction = set(first_alpha)
                uses_follow = False

            prediction_sets.append({
                "left": left,
                "index": idx,
                "production": prod,
                "first_alpha": first_alpha,
                "prediction": prediction,
                "uses_follow": uses_follow
            })

    return prediction_sets


# IMPRESIÓN TIPO INFORME
def imprimir_gramatica(grammar):
    """
    Imprime la gramática en formato legible.
    """
    print("GRAMÁTICA")
    for left, productions in grammar.items():
        right_side = " | ".join(" ".join(prod) for prod in productions)
        print(f"{left} → {right_side}")
    print()


def imprimir_primeros(first_sets):
    """
    Imprime los conjuntos FIRST.
    """
    print("CONJUNTOS DE PRIMEROS")
    for nt in sorted(first_sets.keys()):
        print(f"PRIMEROS({nt}) = {formatear_conjunto(first_sets[nt])}")
    print()


def imprimir_siguientes(follow_sets):
    """
    Imprime los conjuntos FOLLOW.
    """
    print("CONJUNTOS DE SIGUIENTES")
    for nt in sorted(follow_sets.keys()):
        print(f"SIGUIENTES({nt}) = {formatear_conjunto(follow_sets[nt])}")
    print()


def imprimir_prediccion(prediction_sets):
    """
    Imprime los conjuntos de predicción.
    """
    print("CONJUNTOS DE PREDICCIÓN")
    current_left = None

    for item in prediction_sets:
        left = item["left"]
        if left != current_left:
            print(f"{left}:")
            current_left = left

        prod_str = " ".join(item["production"])
        print(f"  {left} → {prod_str}")
        print(f"     PRED = {formatear_conjunto(item['prediction'])}")

    print()


def procesar_gramatica(grammar_text, start_symbol):

    grammar = analizar_gramatica(grammar_text)

    first_sets = calcular_primeros(grammar)
    follow_sets = calcular_siguientes(grammar, first_sets, start_symbol)
    prediction_sets = calcular_prediccion(grammar, first_sets, follow_sets)

    imprimir_gramatica(grammar)
    imprimir_primeros(first_sets)
    imprimir_siguientes(follow_sets)
    imprimir_prediccion(prediction_sets)


# EJEMPLO DE USO
if __name__ == "__main__":
    grammar1 = """
    S -> A uno B C | S dos
    A -> B C D | A tres | ε
    B -> D cuatro C tres | ε
    C -> cinco D B | ε
    D -> seis | ε
    """

    grammar2 = """
    S -> A B uno
    A -> dos B | ε
    B -> C D | tres | ε
    C -> cuatro A B | cinco
    D -> seis | ε
    """

    print("\n========== EJERCICIO 1 ==========\n")
    procesar_gramatica(grammar1, start_symbol="S")

    print("\n========== EJERCICIO 2 ==========\n")
    procesar_gramatica(grammar2, start_symbol="S")