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
