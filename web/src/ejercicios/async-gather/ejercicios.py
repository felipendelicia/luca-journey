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


# Cuántos OK
# `resultados` es una lista donde un fallo se representa con None. Devolvé cuántos NO son None.
# Ejemplo:  cuantos_ok([1, None, 3])  →  2
def cuantos_ok(resultados):
    """Devolvé cuántos resultados no son None."""
    # TU CÓDIGO ACÁ


# Cuántos con error
# Devolvé cuántos resultados son None (fallaron).
def cuantos_error(resultados):
    """Devolvé cuántos resultados son None."""
    # TU CÓDIGO ACÁ


# Solo los OK
# Devolvé una lista con los resultados que NO son None.
# Ejemplo:  solo_ok([1, None, 3])  →  [1, 3]
def solo_ok(resultados):
    """Devolvé los resultados que no son None."""
    # TU CÓDIGO ACÁ


# Emparejar nombres y valores
# Devolvé un dict que asocie cada nombre con su valor (mismas posiciones).
# Ejemplo:  emparejar(["a", "b"], [1, 2])  →  {"a": 1, "b": 2}
def emparejar(nombres, valores):
    """Devolvé un dict nombre → valor."""
    # TU CÓDIGO ACÁ


# Primer OK
# Devolvé el primer resultado que no sea None, o None si todos fallaron.
def primer_ok(resultados):
    """Devolvé el primer resultado no-None, o None."""
    # TU CÓDIGO ACÁ


# Último OK
# Devolvé el último resultado que no sea None, o None si todos fallaron.
def ultimo_ok(resultados):
    """Devolvé el último resultado no-None, o None."""
    # TU CÓDIGO ACÁ


# Reemplazar errores
# Devolvé una lista donde cada None se reemplaza por `default`.
# Ejemplo:  reemplazar_errores([1, None, 3], 0)  →  [1, 0, 3]
def reemplazar_errores(resultados, default):
    """Devolvé los resultados con los None cambiados por default."""
    # TU CÓDIGO ACÁ


# ¿Hubo algún error?
# Devolvé True si algún resultado es None.
def hay_error(resultados):
    """Devolvé True si hay algún None."""
    # TU CÓDIGO ACÁ


# Índice del primer error
# Devolvé el índice del primer None, o -1 si no hay.
def indice_primer_error(resultados):
    """Devolvé el índice del primer None, o -1."""
    # TU CÓDIGO ACÁ


# Suma de los OK
# Devolvé la suma de los resultados que no son None.
# Ejemplo:  suma_ok([1, None, 3])  →  4
def suma_ok(resultados):
    """Devolvé la suma de los no-None."""
    # TU CÓDIGO ACÁ


# Promedio de los OK
# Devolvé el promedio de los resultados no-None, o 0 si no hay ninguno.
def promedio_ok(resultados):
    """Devolvé el promedio de los no-None, o 0."""
    # TU CÓDIGO ACÁ


# Ordenar los OK
# Devolvé los resultados no-None ordenados de menor a mayor.
def ordenar_ok(resultados):
    """Devolvé los no-None ordenados."""
    # TU CÓDIGO ACÁ


# El máximo OK
# Devolvé el mayor de los resultados no-None, o None si no hay ninguno.
def max_ok(resultados):
    """Devolvé el máximo de los no-None, o None."""
    # TU CÓDIGO ACÁ


# ¿Todos fallaron?
# Devolvé True si TODOS los resultados son None.
def todos_fallaron(resultados):
    """Devolvé True si todos son None."""
    # TU CÓDIGO ACÁ


# Con índice
# Devolvé una lista de tuplas (índice, resultado) para cada resultado.
# Ejemplo:  con_indice(["a", "b"])  →  [(0, "a"), (1, "b")]
def con_indice(resultados):
    """Devolvé pares (índice, resultado)."""
    # TU CÓDIGO ACÁ


# Contar valores
# Devolvé un dict valor → cuántas veces aparece (ignorando los None).
# Ejemplo:  contar_valores([1, 1, None, 2])  →  {1: 2, 2: 1}
def contar_valores(resultados):
    """Devolvé un dict valor → cantidad (sin contar None)."""
    # TU CÓDIGO ACÁ
