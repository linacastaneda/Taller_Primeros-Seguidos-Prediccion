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

python calculo.py

---

## Ejemplo de salida

GRAMATICA  
S -> A uno B C | S dos  

CONJUNTOS DE PRIMEROS  
PRIMEROS(A) = { cinco, cuatro, seis, tres, epsilon }  

CONJUNTOS DE SIGUIENTES  
SIGUIENTES(A) = { tres, uno }  

CONJUNTOS DE PREDICCION  
S:  
  S -> A uno B C  
     PRED = { cinco, cuatro, seis, tres, uno }  

ANALISIS DE CONFLICTOS  
La gramatica presenta conflictos LL(1).  

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

## Ejercicios incluidos

Se analizaron dos gramaticas:

Ejercicio 1:  
- Presenta recursion por la izquierda  
- Tiene conflictos LL(1)  

Ejercicio 2:  
- No tiene recursion por la izquierda  
- Presenta conflictos debido a producciones con epsilon  

---
