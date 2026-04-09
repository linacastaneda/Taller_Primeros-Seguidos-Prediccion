# Taller 2 — Análisis Sintáctico Descendente Predictivo

**Lenguajes de Programación y Transducción**  
Universidad Sergio Arboleda · 2026  
Autor: Lina Castañeda

---

## Descripción

Este proyecto implementa en Python los tres algoritmos fundamentales del análisis sintáctico descendente predictivo (LL(1)), tal como se presentan en las diapositivas del curso:

| Algoritmo | Función |
|---|---|
| **PRIMEROS (FIRST)** | Terminales que pueden aparecer al inicio de una cadena derivada de cada no-terminal |
| **SIGUIENTES (FOLLOW)** | Terminales que pueden aparecer inmediatamente después de cada no-terminal en una derivación válida |
| **PREDICCIÓN (PRED)** | Conjunto que determina unívocamente qué producción aplicar dado el terminal de lookahead |

Adicionalmente detecta **recursión izquierda directa** y verifica si la gramática presenta **conflictos LL(1)**.

---

## Estructura del repositorio

```
Taller2_AnálisisSintáctico/
├── analizador_gramatica.py   # Implementación principal (3 algoritmos)
└── README.md                 # Este archivo
```

---

## Requisitos

- Python 3.8 o superior
- Sin dependencias externas (solo biblioteca estándar)

---

## Uso

```bash
python3 analizador_gramatica.py
```

El script procesa automáticamente las dos gramáticas del taller e imprime los resultados en consola.

---

## Gramáticas analizadas

### Ejercicio 1 — Diapositiva 34

```
S → A uno B C  |  S dos
A → B C D  |  A tres  |  ε
B → D cuatro C tres  |  ε
C → cinco D B  |  ε
D → seis  |  ε
```

### Ejercicio 2 — Diapositiva 35

```
S → A B uno
A → dos B  |  ε
B → C D  |  tres  |  ε
C → cuatro A B  |  cinco
D → seis  |  ε
```

---

## Resultados esperados

### Ejercicio 1

| No-terminal | PRIMEROS |
|---|---|
| A | { cinco, cuatro, seis, tres, ε } |
| B | { cuatro, seis, ε } |
| C | { cinco, ε } |
| D | { seis, ε } |
| S | { cinco, cuatro, seis, tres, uno } |

| No-terminal | SIGUIENTES |
|---|---|
| A | { tres, uno } |
| B | { $, cinco, dos, seis, tres, uno } |
| C | { $, dos, seis, tres, uno } |
| D | { $, cuatro, dos, seis, tres, uno } |
| S | { $, dos } |

- **Recursión izquierda directa detectada:** `S → S dos` y `A → A tres`
- **Conflictos LL(1):** Sí (causados por la recursión izquierda)

### Ejercicio 2

| No-terminal | PRIMEROS |
|---|---|
| A | { dos, ε } |
| B | { cinco, cuatro, tres, ε } |
| C | { cinco, cuatro } |
| D | { seis, ε } |
| S | { cinco, cuatro, dos, tres, uno } |

| No-terminal | SIGUIENTES |
|---|---|
| A | { cinco, cuatro, seis, tres, uno } |
| B | { cinco, cuatro, seis, tres, uno } |
| C | { cinco, cuatro, seis, tres, uno } |
| D | { cinco, cuatro, seis, tres, uno } |
| S | { $ } |

- **Recursión izquierda directa:** No se detectó
- **Conflictos LL(1):** Sí (conjuntos de PRED de las producciones de `B` se solapan)

---

## Algoritmos implementados

### PRIMEROS — punto fijo

```python
def calcular_primeros(grammar):
    first = {nt: set() for nt in grammar}
    changed = True
    while changed:
        changed = False
        for head, prods in grammar.items():
            for prod in prods:
                antes = len(first[head])
                first[head] |= primeros_secuencia(prod, first, nts)
                if len(first[head]) > antes:
                    changed = True
    return first
```

### SIGUIENTES — punto fijo

```python
def calcular_siguientes(grammar, first, start):
    follow = {nt: set() for nt in grammar}
    follow[start].add("$")
    changed = True
    while changed:
        changed = False
        for head, prods in grammar.items():
            for prod in prods:
                for i, sym in enumerate(prod):
                    if sym not in nts: continue
                    beta = prod[i+1:]
                    first_beta = primeros_secuencia(beta, first, nts)
                    antes = len(follow[sym])
                    follow[sym] |= (first_beta - {"ε"})
                    if not beta or "ε" in first_beta:
                        follow[sym] |= follow[head]
                    if len(follow[sym]) > antes:
                        changed = True
    return follow
```

### PREDICCIÓN — por producción

```python
def calcular_prediccion(grammar, first, follow):
    for head, prods in grammar.items():
        for prod in prods:
            first_alpha = primeros_secuencia(prod, first, nts)
            if "ε" in first_alpha:
                pred = (first_alpha - {"ε"}) | follow[head]
            else:
                pred = set(first_alpha)
```

---

## Formato de gramática (entrada)

Las gramáticas se definen como texto con el formato:

```
NoTerminal -> simbolo1 simbolo2 | alternativa1 alternativa2
```

- Los **terminales** se escriben en minúscula (ej. `uno`, `dos`, `tres`).
- Los **no-terminales** son los que aparecen como claves del diccionario.
- La cadena vacía se indica con `ε`.