"""🥞 Ejercicios — Pila (stack)

Una pila es LIFO: el último que entra es el primero que sale (como una pila de platos).
Se usa para deshacer acciones, evaluar paréntesis, recorrer en profundidad…
✅ Corregí cuando termines.
"""


# Apilar
# Poné `x` ARRIBA de la pila (una lista) y devolvé la pila.
# Ejemplo:  apilar([1, 2], 3)  →  [1, 2, 3]
def apilar(pila, x):
    """Agregá x al tope y devolvé la pila."""


# Desapilar (LIFO)
# Sacá y devolvé el elemento de ARRIBA (el último). Si está vacía, devolvé None.
# Ejemplo:  desapilar([1, 2, 3])  →  3  (la pila queda [1, 2])
def desapilar(pila):
    """Sacá y devolvé el tope, o None si está vacía."""


# Ver el tope
# Devolvé el elemento de arriba SIN sacarlo. Si está vacía, devolvé None.
# Ejemplo:  tope([1, 2, 3])  →  3   ·   tope([])  →  None
def tope(pila):
    """Devolvé el tope sin sacarlo."""


# ¿Paréntesis balanceados?
# Usando una pila, devolvé True si los paréntesis del texto están bien balanceados.
# Cada "(" debe cerrar con un ")". Ejemplo:  balanceado("(a(b)c)")  →  True
#           balanceado("(a(b)")  →  False   ·   balanceado(")(")  →  False
def balanceado(texto):
    """Devolvé True si los paréntesis están balanceados."""
