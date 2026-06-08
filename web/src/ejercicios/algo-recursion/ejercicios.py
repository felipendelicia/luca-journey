"""🔁 Ejercicios — Recursión

Una función recursiva se llama a sí misma con un problema más chico, hasta llegar a un
CASO BASE que la frena. Sin caso base, se cuelga. ✅ Corregí cuando termines.
"""


# Factorial
# n! = n × (n-1) × … × 1. El caso base: factorial(0) es 1.
# Resolvelo de forma RECURSIVA (la función se llama a sí misma).
# Ejemplo:  factorial(5)  →  120   ·   factorial(0)  →  1
def factorial(n):
    """Devolvé n! de forma recursiva."""


# Suma hasta n
# Devolvé 1 + 2 + … + n de forma recursiva. Caso base: suma_hasta(0) es 0.
# Ejemplo:  suma_hasta(4)  →  10   ·   suma_hasta(0)  →  0
def suma_hasta(n):
    """Devolvé la suma de 1..n de forma recursiva."""


# Fibonacci
# La sucesión: 0, 1, 1, 2, 3, 5, 8, … Cada número es la suma de los dos anteriores.
# Casos base: fibonacci(0) = 0, fibonacci(1) = 1. Resolvelo recursivamente.
# Ejemplo:  fibonacci(6)  →  8   ·   fibonacci(0)  →  0
def fibonacci(n):
    """Devolvé el n-ésimo Fibonacci de forma recursiva."""


# Potencia
# Devolvé base elevado a exp (exp >= 0) de forma recursiva. Caso base: potencia(b, 0) = 1.
# Ejemplo:  potencia(2, 5)  →  32   ·   potencia(7, 0)  →  1
def potencia(base, exp):
    """Devolvé base**exp de forma recursiva."""


# Cuenta regresiva
# Devolvé "n,n-1,…,1,Ya!" usando recursión (sin bucles). Caso base: n<=0 → "Ya!".
# Ejemplo:  cuenta_regresiva(3)  →  "3,2,1,Ya!"
def cuenta_regresiva(n):
    """Devolvé la cuenta regresiva como texto, con recursión."""
    # TU CÓDIGO ACÁ


# Suma de una lista
# Devolvé la suma de los elementos con recursión (sin sum() ni bucles).
# Ejemplo:  suma_lista([1, 2, 3])  →  6   ·   suma_lista([])  →  0
def suma_lista(lista):
    """Devolvé la suma de la lista, con recursión."""
    # TU CÓDIGO ACÁ


# Largo de una lista
# Devolvé cuántos elementos tiene, con recursión (sin len()).
# Ejemplo:  largo([10, 20, 30])  →  3
def largo(lista):
    """Devolvé el largo de la lista, con recursión."""
    # TU CÓDIGO ACÁ


# Máximo de una lista
# Devolvé el valor más grande con recursión (sin max()). Asumí que no está vacía.
# Ejemplo:  maximo([3, 9, 1])  →  9
def maximo(lista):
    """Devolvé el máximo, con recursión."""
    # TU CÓDIGO ACÁ


# Invertir texto
# Devolvé el texto al revés, con recursión.
# Ejemplo:  invertir_texto("pika")  →  "akip"
def invertir_texto(texto):
    """Devolvé el texto al revés, con recursión."""
    # TU CÓDIGO ACÁ


# Palíndromo
# Devolvé True si el texto se lee igual al derecho y al revés. Resolvelo comparando el primer
# y el último carácter y recurriendo sobre el medio.
# Ejemplo:  es_palindromo("ana")  →  True   ·   es_palindromo("pika")  →  False
def es_palindromo(texto):
    """Devolvé True si el texto es palíndromo, con recursión."""
    # TU CÓDIGO ACÁ


# Contar apariciones
# Devolvé cuántas veces aparece `x` en la lista, con recursión.
# Ejemplo:  contar_apariciones([1, 2, 1, 1], 1)  →  3
def contar_apariciones(lista, x):
    """Devolvé cuántas veces está x, con recursión."""
    # TU CÓDIGO ACÁ


# Multiplicar sumando
# Devolvé a × b usando SOLO sumas y recursión (sin el operador *). Asumí b >= 0.
# Ejemplo:  multiplicar(4, 3)  →  12
def multiplicar(a, b):
    """Devolvé a*b sumando a, con recursión."""
    # TU CÓDIGO ACÁ


# Máximo común divisor
# Devolvé el MCD de a y b con el método de Euclides recursivo: mcd(a, b) = mcd(b, a % b),
# caso base b == 0 → a.
# Ejemplo:  mcd(12, 8)  →  4
def mcd(a, b):
    """Devolvé el MCD de a y b, con recursión (Euclides)."""
    # TU CÓDIGO ACÁ


# Suma de dígitos
# Devolvé la suma de los dígitos de `n` con recursión.
# Ejemplo:  suma_digitos(253)  →  10
def suma_digitos(n):
    """Devolvé la suma de los dígitos de n, con recursión."""
    # TU CÓDIGO ACÁ


# Aplanar listas anidadas
# `lista` puede tener listas adentro (a cualquier profundidad). Devolvé una lista PLANA con
# todos los valores, en orden, con recursión.
# Ejemplo:  aplanar([1, [2, [3, 4]], 5])  →  [1, 2, 3, 4, 5]
def aplanar(lista):
    """Devolvé la lista aplanada, con recursión."""
    # TU CÓDIGO ACÁ


# Número combinatorio
# Devolvé C(n, k) (combinaciones) con la regla de Pascal recursiva:
# C(n,k) = C(n-1,k-1) + C(n-1,k), con C(n,0) = C(n,n) = 1.
# Ejemplo:  binomial(5, 2)  →  10
def binomial(n, k):
    """Devolvé el número combinatorio C(n,k), con recursión."""
    # TU CÓDIGO ACÁ


# Torres de Hanói (movimientos)
# Devolvé cuántos movimientos se necesitan para mover `n` discos: mover n discos = mover
# n-1, mover 1, mover n-1. Caso base n == 0 → 0.
# Ejemplo:  hanoi_movimientos(3)  →  7
def hanoi_movimientos(n):
    """Devolvé la cantidad de movimientos de Hanói, con recursión."""
    # TU CÓDIGO ACÁ


# Búsqueda binaria recursiva
# `ordenada` viene de menor a mayor. Devolvé el índice de `x` con búsqueda binaria recursiva,
# o -1 si no está.
# Ejemplo:  busqueda_binaria_rec([1, 3, 5, 7, 9], 7)  →  3
def busqueda_binaria_rec(ordenada, x):
    """Devolvé el índice de x con búsqueda binaria recursiva, o -1."""
    # TU CÓDIGO ACÁ


# Contar pares
# Devolvé cuántos números PARES hay en la lista, con recursión.
# Ejemplo:  contar_pares([1, 2, 4, 7, 8])  →  3
def contar_pares(lista):
    """Devolvé cuántos pares hay, con recursión."""
    # TU CÓDIGO ACÁ


# Cantidad de dígitos
# Devolvé cuántos dígitos tiene `n` (n >= 0), con recursión.
# Ejemplo:  cantidad_digitos(2025)  →  4   ·   cantidad_digitos(7)  →  1
def cantidad_digitos(n):
    """Devolvé cuántos dígitos tiene n, con recursión."""
    # TU CÓDIGO ACÁ
