"""✏️ Ejercicios — Errores: try / except

Los errores pasan. Un buen programa no explota: los ATRAPA con try/except y sigue.
✅ Corregir al terminar.
"""


# Dividir sin explotar
# Dividí a/b, pero si b es 0 devolvé None (en vez de romper). Pista: try/except ZeroDivisionError.
# Ejemplo:  dividir_seguro(10, 2)  →  5.0   ·   dividir_seguro(5, 0)  →  None
def dividir_seguro(a, b):
    """Devolvé a / b, o None si b es 0."""
    # TU CÓDIGO ACÁ
    pass


# Convertir sin fallar
# Convertí un texto a int. Si no se puede, devolvé 0. Pista: try/except ValueError.
# Ejemplo:  a_entero("42")  →  42   ·   a_entero("pikachu")  →  0
def a_entero(texto):
    """Devolvé int(texto), o 0 si falla."""
    # TU CÓDIGO ACÁ
    pass


# Posición segura
# Devolvé lista[i]. Si la posición no existe, devolvé None. Pista: try/except IndexError.
# Ejemplo:  elemento([10, 20, 30], 1)  →  20   ·   elemento([10], 5)  →  None
def elemento(lista, i):
    """Devolvé lista[i], o None si no existe."""
    # TU CÓDIGO ACÁ
    pass


# Clave segura
# Devolvé dic[clave]. Si la clave no existe, devolvé "no encontrado". Pista: try/except KeyError.
# Ejemplo:  valor({"nivel": 25}, "tipo")  →  "no encontrado"
def valor(dic, clave):
    """Devolvé dic[clave], o "no encontrado" si no está."""
    # TU CÓDIGO ACÁ
    pass


# Raíz segura
# Devolvé la raíz cuadrada de n. Si n es negativo (no tiene raíz real), atrapá el error y
# devolvé None.  Ejemplo:  raiz_segura(9)  →  3.0   ·   raiz_segura(-4)  →  None
def raiz_segura(n):
    """Devolvé la raíz de n, o None si no se puede."""
    # TU CÓDIGO ACÁ
    pass


# Promedio seguro
# Devolvé el promedio de la lista. Si está vacía, atrapá el error y devolvé 0.
# Ejemplo:  promedio_seguro([2, 4])  →  3.0   ·   promedio_seguro([])  →  0
def promedio_seguro(lista):
    """Devolvé el promedio, o 0 si la lista está vacía."""
    # TU CÓDIGO ACÁ
    pass


# Primer elemento
# Devolvé el primer elemento. Si la lista está vacía, devolvé None.
# Ejemplo:  primer_elemento([10, 20])  →  10   ·   primer_elemento([])  →  None
def primer_elemento(lista):
    """Devolvé el primer elemento, o None."""
    # TU CÓDIGO ACÁ
    pass


# A float seguro
# Convertí el texto a float. Si no se puede, devolvé None.
# Ejemplo:  a_float_seguro("3.5")  →  3.5   ·   a_float_seguro("pika")  →  None
def a_float_seguro(texto):
    """Devolvé float(texto), o None si falla."""
    # TU CÓDIGO ACÁ
    pass


# Dividir una lista
# Dividí cada número de la lista por `divisor` y devolvé la lista de resultados. Si `divisor`
# es 0, devolvé None.  Ejemplo:  dividir_lista([10, 20], 2)  →  [5.0, 10.0]
def dividir_lista(numeros, divisor):
    """Devolvé cada número dividido por divisor, o None si divisor es 0."""
    # TU CÓDIGO ACÁ
    pass


# Buscar índice
# Devolvé la posición de `x` en la lista. Si no está, devolvé -1 (atrapá el error de .index).
# Ejemplo:  buscar_indice(["a", "b"], "b")  →  1   ·   buscar_indice(["a"], "z")  →  -1
def buscar_indice(lista, x):
    """Devolvé el índice de x, o -1 si no está."""
    # TU CÓDIGO ACÁ
    pass


# Convertir todos
# Convertí cada texto de la lista a int; los que no se pueden, ponelos en 0.
# Ejemplo:  convertir_todos(["1", "x", "3"])  →  [1, 0, 3]
def convertir_todos(textos):
    """Devolvé cada texto como int, o 0 si no se puede."""
    # TU CÓDIGO ACÁ
    pass


# Acceso anidado
# `claves` es una lista de claves para entrar a un dict adentro de otro. Devolvé el valor final,
# o None si en el camino falta alguna clave.
# Ejemplo:  acceso_anidado({"a": {"b": 9}}, ["a", "b"])  →  9
#           acceso_anidado({"a": {"b": 9}}, ["a", "z"])  →  None
def acceso_anidado(dic, claves):
    """Devolvé el valor anidado, o None si falta alguna clave."""
    # TU CÓDIGO ACÁ
    pass


# Dividir o avisar
# Devolvé a / b, o el texto "no se puede dividir por cero" si b es 0.
# Ejemplo:  dividir_o_mensaje(6, 2)  →  3.0   ·   dividir_o_mensaje(6, 0)  →  "no se puede dividir por cero"
def dividir_o_mensaje(a, b):
    """Devolvé a/b o un mensaje si b es 0."""
    # TU CÓDIGO ACÁ
    pass


# Sumar los válidos
# Sumá solo los textos que se pueden convertir a int; ignorá los que no.
# Ejemplo:  sumar_validos(["10", "x", "5"])  →  15
def sumar_validos(textos):
    """Devolvé la suma de los textos convertibles a int."""
    # TU CÓDIGO ACÁ
    pass


# Máximo seguro
# Devolvé el máximo de la lista, o None si está vacía.
# Ejemplo:  max_seguro([3, 9, 1])  →  9   ·   max_seguro([])  →  None
def max_seguro(lista):
    """Devolvé el máximo, o None si está vacía."""
    # TU CÓDIGO ACÁ
    pass


# Leer o cero
# Devolvé dic[clave]; si la clave no existe, devolvé 0.
# Ejemplo:  leer_o_cero({"hp": 35}, "hp")  →  35   ·   leer_o_cero({}, "hp")  →  0
def leer_o_cero(dic, clave):
    """Devolvé dic[clave], o 0 si no está."""
    # TU CÓDIGO ACÁ
    pass


# Ejecutar seguro
# Llamá a `func(x)`. Si tira CUALQUIER error, devolvé None en vez de explotar.
# Ejemplo:  ejecutar_seguro(int, "42")  →  42   ·   ejecutar_seguro(int, "pika")  →  None
def ejecutar_seguro(func, x):
    """Devolvé func(x), o None si tira error."""
    # TU CÓDIGO ACÁ
    pass


# Cuántos válidos
# Devolvé cuántos textos de la lista se pueden convertir a int.
# Ejemplo:  cuantos_validos(["1", "x", "3", "y"])  →  2
def cuantos_validos(textos):
    """Devolvé cuántos textos son enteros válidos."""
    # TU CÓDIGO ACÁ
    pass


# Último elemento
# Devolvé el último elemento, o None si la lista está vacía.
# Ejemplo:  ultimo_elemento([1, 2, 3])  →  3   ·   ultimo_elemento([])  →  None
def ultimo_elemento(lista):
    """Devolvé el último elemento, o None."""
    # TU CÓDIGO ACÁ
    pass


# A entero o por defecto
# Convertí el texto a int; si no se puede, devolvé `default`.
# Ejemplo:  a_entero_o("42", 0)  →  42   ·   a_entero_o("pika", -1)  →  -1
def a_entero_o(texto, default):
    """Devolvé int(texto), o default si falla."""
    # TU CÓDIGO ACÁ
    pass
