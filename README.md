# Analisis de Gramaticas: PRIMEROS, SIGUIENTES y PREDICCION

## Descripcion

Este proyecto implementa el calculo de los conjuntos de PRIMEROS, SIGUIENTES y PREDICCION para gramaticas libres de contexto, siguiendo los algoritmos vistos en clase de Procesadores de Lenguaje.

El programa tambien determina si la gramatica presenta conflictos LL(1).

---

## Funcionalidades

El programa permite:

- Parsear una gramatica escrita en texto.
- Calcular los conjuntos de:
  - PRIMEROS
  - SIGUIENTES
  - PREDICCION
- Mostrar los resultados en formato tipo informe.
- Detectar si la gramatica tiene conflictos LL(1).

---

## Conceptos implementados

### PRIMEROS

Determina los terminales que pueden aparecer al inicio de una derivacion de un simbolo.

### SIGUIENTES

Determina los terminales que pueden aparecer inmediatamente despues de un no terminal.

### PREDICCION

Se usa para analisis sintactico predictivo.

Si epsilon pertenece a PRIMEROS(alpha):

PRED(A -> alpha) = (PRIMEROS(alpha) - {epsilon}) union SIGUIENTES(A)

Si epsilon no pertenece a PRIMEROS(alpha):

PRED(A -> alpha) = PRIMEROS(alpha)

---

## Formato de la gramatica

La gramatica debe escribirse de la siguiente forma:

S -> A uno B C | S dos  
A -> B C D | A tres | epsilon  
B -> D cuatro C tres | epsilon  
C -> cinco D B | epsilon  
D -> seis | epsilon  

Reglas:

- Usar "->" para producciones
- Usar "|" para separar alternativas
- Separar simbolos con espacios
- Usar "epsilon" o "ε" para representar epsilon

---

## Ejecucion

Para ejecutar el programa:

```bash
python3 analizador_gramatica.py
```

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

## Estructura del codigo

El archivo principal contiene las siguientes funciones:

- analizar_gramatica: parsea la gramatica desde texto  
- calcular_primeros: calcula los conjuntos PRIMEROS  
- calcular_siguientes: calcula los conjuntos SIGUIENTES  
- calcular_prediccion: calcula los conjuntos de PREDICCION  
- detectar_conflictos_ll1: verifica si hay conflictos LL(1)  
- funciones de impresion para mostrar resultados  

---

## Formato de gramática (entrada)

Las gramáticas se definen como texto con el formato:

```
NoTerminal -> simbolo1 simbolo2 | alternativa1 alternativa2
```

- Los **terminales** se escriben en minúscula (ej. `uno`, `dos`, `tres`).
- Los **no-terminales** son los que aparecen como claves del diccionario.
- La cadena vacía se indica con `ε`.
---
