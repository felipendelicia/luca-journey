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


# ¿Pila vacía?
# Devolvé True si la pila no tiene elementos.
# Ejemplo:  esta_vacia([])  →  True   ·   esta_vacia([1])  →  False
def esta_vacia(pila):
    """Devolvé True si la pila está vacía."""
    # TU CÓDIGO ACÁ


# Tamaño
# Devolvé cuántos elementos tiene la pila.
# Ejemplo:  tamano([1, 2, 3])  →  3
def tamano(pila):
    """Devolvé la cantidad de elementos."""
    # TU CÓDIGO ACÁ


# Tope seguro
# Devolvé el elemento de arriba SIN sacarlo. Si la pila está vacía, devolvé None.
# Ejemplo:  tope_seguro([1, 2, 3])  →  3   ·   tope_seguro([])  →  None
def tope_seguro(pila):
    """Devolvé el tope, o None si está vacía."""
    # TU CÓDIGO ACÁ


# Apilar varios
# Apilá todos los `elementos` (en orden) sobre la pila y devolvé la pila.
# Ejemplo:  apilar_varios([1], [2, 3])  →  [1, 2, 3]
def apilar_varios(pila, elementos):
    """Apilá todos los elementos y devolvé la pila."""
    # TU CÓDIGO ACÁ


# Vaciar
# Sacá todos los elementos uno por uno y devolvelos en una lista, en el orden en que salen
# (el de arriba primero).
# Ejemplo:  vaciar([1, 2, 3])  →  [3, 2, 1]
def vaciar(pila):
    """Devolvé los elementos en el orden en que salen."""
    # TU CÓDIGO ACÁ


# Invertir con pila
# Devolvé una lista NUEVA al revés, usando una pila (apilá todo y luego desapilá).
# Ejemplo:  invertir([1, 2, 3])  →  [3, 2, 1]
def invertir(lista):
    """Devolvé la lista al revés usando una pila."""
    # TU CÓDIGO ACÁ


# Balanceo de todo tipo
# Devolvé True si los paréntesis (), corchetes [] y llaves {} están bien balanceados y
# anidados. Ejemplo:  balanceado_todo("([]{})")  →  True   ·   balanceado_todo("([)]")  →  False
def balanceado_todo(texto):
    """Devolvé True si (), [] y {} están bien balanceados."""
    # TU CÓDIGO ACÁ


# Profundidad máxima
# Devolvé el nivel máximo de anidamiento de paréntesis.
# Ejemplo:  profundidad_maxima("((()))")  →  3   ·   profundidad_maxima("()()")  →  1
def profundidad_maxima(texto):
    """Devolvé el anidamiento máximo de paréntesis."""
    # TU CÓDIGO ACÁ


# Calculadora postfija (RPN)
# `tokens` es una lista como ["3", "4", "+"]: números y operadores +, -, *. Evaluala con una
# pila (al ver un operador, sacás dos números y apilás el resultado). Devolvé el número final.
# Ejemplo:  evaluar_postfija(["3", "4", "+", "2", "*"])  →  14
def evaluar_postfija(tokens):
    """Evaluá la expresión postfija y devolvé el resultado."""
    # TU CÓDIGO ACÁ


# Decimal a binario
# Devolvé la representación binaria de `n` como string, usando una pila (restos de dividir por 2).
# Ejemplo:  decimal_a_binario(6)  →  "110"   ·   decimal_a_binario(0)  →  "0"
def decimal_a_binario(n):
    """Devolvé n en binario, como string."""
    # TU CÓDIGO ACÁ


# Quitar adyacentes iguales
# Recorré el texto con una pila: si el carácter es igual al de arriba, sacás ese; si no, lo
# apilás. Devolvé el texto resultante.
# Ejemplo:  quitar_adyacentes("abbac")  →  "c"   ·   quitar_adyacentes("abc")  →  "abc"
def quitar_adyacentes(texto):
    """Devolvé el texto sin pares adyacentes iguales (con pila)."""
    # TU CÓDIGO ACÁ


# Palíndromo con pila
# Devolvé True si el texto se lee igual al derecho y al revés, comparándolo contra su
# versión invertida con una pila.
# Ejemplo:  es_palindromo_pila("ana")  →  True   ·   es_palindromo_pila("pikachu")  →  False
def es_palindromo_pila(texto):
    """Devolvé True si el texto es palíndromo."""
    # TU CÓDIGO ACÁ


# Simular una pila
# `operaciones` es una lista de strings: "push N" apila el número N, "pop" saca el de arriba
# (si hay). Devolvé la pila final.
# Ejemplo:  simular_pila(["push 3", "pop", "push 5"])  →  [5]
def simular_pila(operaciones):
    """Aplicá las operaciones y devolvé la pila final."""
    # TU CÓDIGO ACÁ


# Invertir texto con pila
# Devolvé el texto al revés usando una pila.
# Ejemplo:  invertir_texto("pika")  →  "akip"
def invertir_texto(texto):
    """Devolvé el texto al revés usando una pila."""
    # TU CÓDIGO ACÁ


# Pares completos
# Devolvé cuántos pares de paréntesis () cierran correctamente.
# Ejemplo:  pares_completos("(())")  →  2   ·   pares_completos("(()")  →  1
def pares_completos(texto):
    """Devolvé cuántos pares () cierran bien."""
    # TU CÓDIGO ACÁ


# Sin cerrar
# Devolvé cuántos '(' quedan SIN cerrar al final.
# Ejemplo:  sin_cerrar("(()")  →  1   ·   sin_cerrar("()")  →  0
def sin_cerrar(texto):
    """Devolvé cuántos '(' quedan sin cerrar."""
    # TU CÓDIGO ACÁ
