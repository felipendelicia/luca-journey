"""🪢 Ejercicios — Juntar resultados (gather)

`asyncio.gather` lanza varias corrutinas juntas y te devuelve TODOS los resultados, en
el mismo orden en que las pediste. Acá procesás esos resultados. ✅ Corregí al terminar.
"""


# Combinar nombre → valor
# `resultados` es una lista de tuplas (nombre, valor). Devolvé un dict {nombre: valor}.
# Ejemplo:  combinar([("pikachu", 100), ("onix", 80)])  →  {"pikachu": 100, "onix": 80}
def combinar(resultados):
    """Devolvé un dict a partir de las tuplas (nombre, valor)."""


# Emparejar en orden
# gather conserva el orden: el resultado i corresponde a la tarea i. Recibís `nombres` y
# `valores` (dos listas alineadas) y devolvés un dict emparejándolos por posición.
# Ejemplo:  en_orden(["a", "b"], [1, 2])  →  {"a": 1, "b": 2}
def en_orden(nombres, valores):
    """Devolvé un dict emparejando nombres con valores por posición."""


# ¿Salieron todos bien?
# Una tarea que falló deja None en su lugar. Devolvé True si NINGÚN resultado es None.
# Ejemplo:  todos_ok([1, 2, 3])  →  True   ·   todos_ok([1, None, 3])  →  False
def todos_ok(resultados):
    """Devolvé True si no hay ningún None."""


# Primer error
# Devolvé el índice del primer resultado que sea None, o -1 si están todos bien.
# Ejemplo:  primer_error([1, None, 3])  →  1   ·   primer_error([1, 2])  →  -1
def primer_error(resultados):
    """Devolvé el índice del primer None, o -1."""
