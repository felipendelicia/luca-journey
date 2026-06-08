"""🗂️ Ejercicios — Diccionarios y sets

Los diccionarios (hash maps) y los sets buscan en tiempo casi instantáneo. Son la
herramienta para contar, deduplicar y comparar colecciones. ✅ Corregí cuando termines.
"""


# Frecuencias
# Contá cuántas veces aparece cada elemento y devolvé un dict elemento → cantidad.
# Ejemplo:  frecuencias(["a", "b", "a", "c", "a"])  →  {"a": 3, "b": 1, "c": 1}
def frecuencias(items):
    """Devolvé un dict con la cantidad de cada elemento."""


# Sin duplicados
# Devolvé la lista sin repetidos, MANTENIENDO el orden de la primera aparición.
# Ejemplo:  sin_duplicados([3, 1, 3, 2, 1])  →  [3, 1, 2]
def sin_duplicados(items):
    """Devolvé los elementos únicos, en orden de aparición."""


# El más común
# Devolvé el elemento que más se repite. Si hay empate, devolvé el que aparece primero.
# Ejemplo:  mas_comun(["a", "b", "a", "c"])  →  "a"
def mas_comun(items):
    """Devolvé el elemento más frecuente."""


# Intersección
# Devolvé los elementos que están en AMBAS listas, sin repetidos y ORDENADOS.
# Ejemplo:  interseccion([1, 2, 3, 4], [2, 4, 6])  →  [2, 4]
def interseccion(a, b):
    """Devolvé los elementos comunes, únicos y ordenados."""


# Unión
# Devolvé una lista ORDENADA con todos los elementos que están en `a` o en `b`, sin repetir.
# Ejemplo:  union([1, 2], [2, 3])  →  [1, 2, 3]
def union(a, b):
    """Devolvé la unión de a y b, ordenada y sin repetir."""
    # TU CÓDIGO ACÁ


# Diferencia
# Devolvé una lista ORDENADA con los elementos que están en `a` pero NO en `b`.
# Ejemplo:  diferencia([1, 2, 3], [2])  →  [1, 3]
def diferencia(a, b):
    """Devolvé los elementos de a que no están en b, ordenados."""
    # TU CÓDIGO ACÁ


# ¿Mismos elementos?
# Devolvé True si `a` y `b` tienen exactamente los mismos elementos (sin importar el orden
# ni las repeticiones).  Ejemplo:  mismos_elementos([1, 2, 2], [2, 1])  →  True
def mismos_elementos(a, b):
    """Devolvé True si a y b tienen los mismos elementos."""
    # TU CÓDIGO ACÁ


# Únicos en orden
# Devolvé los elementos SIN repetir, en el orden en que aparecieron por primera vez.
# Ejemplo:  unicos([3, 1, 3, 2, 1])  →  [3, 1, 2]
def unicos(items):
    """Devolvé los elementos sin repetir, en orden de aparición."""
    # TU CÓDIGO ACÁ


# Contar distintos
# Devolvé cuántos valores DIFERENTES hay.  Ejemplo:  contar_distintos([1, 1, 2, 3, 3])  →  3
def contar_distintos(items):
    """Devolvé cuántos valores distintos hay."""
    # TU CÓDIGO ACÁ


# Agrupar por inicial
# `palabras` es una lista de strings. Devolvé un dict: primera letra → lista de palabras que
# empiezan con ella (en orden de aparición).
# Ejemplo:  agrupar_por_inicial(["pikachu", "onix", "pidgey"])
#               →  {"p": ["pikachu", "pidgey"], "o": ["onix"]}
def agrupar_por_inicial(palabras):
    """Devolvé un dict inicial → lista de palabras."""
    # TU CÓDIGO ACÁ


# Invertir un diccionario
# Devolvé un dict con las claves y valores intercambiados (asumí valores únicos).
# Ejemplo:  invertir_dict({"a": 1, "b": 2})  →  {1: "a", 2: "b"}
def invertir_dict(d):
    """Devolvé el diccionario con clave y valor intercambiados."""
    # TU CÓDIGO ACÁ


# Claves con cierto valor
# Devolvé una lista con las claves cuyo valor sea igual a `v`.
# Ejemplo:  claves_con_valor({"a": 1, "b": 2, "c": 1}, 1)  →  ["a", "c"]
def claves_con_valor(d, v):
    """Devolvé las claves cuyo valor es v."""
    # TU CÓDIGO ACÁ


# Suma de los valores
# Devolvé la suma de todos los valores del diccionario.
# Ejemplo:  suma_valores({"a": 10, "b": 5})  →  15
def suma_valores(d):
    """Devolvé la suma de los valores."""
    # TU CÓDIGO ACÁ


# Clave con el mayor valor
# Devolvé la clave cuyo valor es el más grande.
# Ejemplo:  clave_mayor_valor({"pikachu": 5, "onix": 12})  →  "onix"
def clave_mayor_valor(d):
    """Devolvé la clave del valor máximo."""
    # TU CÓDIGO ACÁ


# Combinar conteos
# `a` y `b` son diccionarios de conteos. Devolvé uno nuevo que SUME los valores de las claves
# repetidas.  Ejemplo:  combinar_conteos({"x": 1}, {"x": 2, "y": 5})  →  {"x": 3, "y": 5}
def combinar_conteos(a, b):
    """Devolvé un dict que sume los conteos de a y b."""
    # TU CÓDIGO ACÁ


# ¿Anagramas?
# Devolvé True si `a` y `b` tienen exactamente las mismas letras (mismas cantidades).
# Ejemplo:  son_anagramas("roma", "amor")  →  True   ·   son_anagramas("ash", "gary")  →  False
def son_anagramas(a, b):
    """Devolvé True si a y b son anagramas."""
    # TU CÓDIGO ACÁ


# Los que faltan
# Devolvé una lista ORDENADA con los elementos de `esperados` que NO están en `tengo`.
# Ejemplo:  faltantes([1, 2, 3, 4], [2, 4])  →  [1, 3]
def faltantes(esperados, tengo):
    """Devolvé los esperados que no están en tengo, ordenados."""
    # TU CÓDIGO ACÁ


# Los que aparecen una sola vez
# Devolvé una lista con los elementos que aparecen EXACTAMENTE una vez, en orden de aparición.
# Ejemplo:  aparece_una_vez([1, 2, 2, 3, 1, 4])  →  [3, 4]
def aparece_una_vez(items):
    """Devolvé los elementos que aparecen una sola vez."""
    # TU CÓDIGO ACÁ


# ¿Tiene todas las claves?
# Devolvé True si TODAS las `claves` están en el diccionario `d`.
# Ejemplo:  tiene_todas({"a": 1, "b": 2}, ["a", "b"])  →  True
def tiene_todas(d, claves):
    """Devolvé True si d tiene todas las claves."""
    # TU CÓDIGO ACÁ


# Los dos más comunes
# Devolvé una lista con los DOS elementos que más se repiten (del más al menos común).
# Ejemplo:  dos_mas_comunes([1, 1, 2, 2, 2, 3])  →  [2, 1]
def dos_mas_comunes(items):
    """Devolvé los dos elementos más frecuentes."""
    # TU CÓDIGO ACÁ
