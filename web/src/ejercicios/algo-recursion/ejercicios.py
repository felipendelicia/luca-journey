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
