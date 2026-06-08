"""🤖 Ejercicios — Automatizador (bot)

Un bot encadena pasos: normaliza datos, los filtra y los agrupa. Acá practicás ese
"pipeline" sobre una lista de Pokémon (cada uno un dict). ✅ Corregí cuando termines.
"""


# Normalizar un nombre
# Devolvé el nombre sin espacios al borde y en minúsculas (para comparar sin líos).
# Ejemplo:  normalizar("  Pikachu ")  →  "pikachu"
def normalizar(nombre):
    """Devolvé el nombre limpio y en minúsculas."""


# Filtrar por nivel
# `pokes` es una lista de dicts con clave "nivel". Devolvé solo los que tengan
# nivel mayor o igual a `minimo`.
# Ejemplo:  filtrar_nivel([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}], 10)
#               →  [{"nombre": "b", "nivel": 20}]
def filtrar_nivel(pokes, minimo):
    """Devolvé los pokes con nivel >= minimo."""


# Agrupar por tipo
# Cada poke es un dict con "nombre" y "tipo". Devolvé un dict que para cada tipo liste
# los NOMBRES de los Pokémon de ese tipo (en el orden en que aparecen).
# Ejemplo:  agrupar_por_tipo([{"nombre": "Squirtle", "tipo": "agua"},
#                             {"nombre": "Charmander", "tipo": "fuego"},
#                             {"nombre": "Psyduck", "tipo": "agua"}])
#               →  {"agua": ["Squirtle", "Psyduck"], "fuego": ["Charmander"]}
def agrupar_por_tipo(pokes):
    """Devolvé un dict tipo → lista de nombres."""


# Contar
# Devolvé cuántos Pokémon hay en la lista.
# Ejemplo:  contar([{"nombre": "a"}, {"nombre": "b"}])  →  2
def contar(pokes):
    """Devolvé la cantidad de pokes."""


# Normalizar una lista
# Devolvé cada nombre sin espacios al borde y en minúsculas.
# Ejemplo:  normalizar_lista(["  Pikachu", "ONIX "])  →  ["pikachu", "onix"]
def normalizar_lista(nombres):
    """Devolvé los nombres normalizados."""
    # TU CÓDIGO ACÁ


# Quitar duplicados
# Devolvé los nombres sin repetir, en orden de aparición.
def quitar_duplicados(nombres):
    """Devolvé los nombres sin repetir."""
    # TU CÓDIGO ACÁ


# Solo nombres
# Devolvé una lista con el "nombre" de cada poke.
def solo_nombres(pokes):
    """Devolvé los nombres de los pokes."""
    # TU CÓDIGO ACÁ


# Ordenar por nivel
# Devolvé los pokes ordenados de mayor a menor nivel.
def ordenar_por_nivel(pokes):
    """Devolvé los pokes ordenados por nivel (desc)."""
    # TU CÓDIGO ACÁ


# El de mayor nivel
# Devolvé el dict del poke con nivel más alto.
def el_de_mayor_nivel(pokes):
    """Devolvé el poke de mayor nivel."""
    # TU CÓDIGO ACÁ


# Nivel promedio
# Devolvé el promedio de los niveles.
def nivel_promedio(pokes):
    """Devolvé el nivel promedio."""
    # TU CÓDIGO ACÁ


# Tipos únicos
# Devolvé una lista ORDENADA con los tipos distintos.
def tipos_unicos(pokes):
    """Devolvé los tipos distintos, ordenados."""
    # TU CÓDIGO ACÁ


# Filtrar por tipo
# Devolvé los pokes cuyo "tipo" sea `tipo`.
def filtrar_tipo(pokes, tipo):
    """Devolvé los pokes de ese tipo."""
    # TU CÓDIGO ACÁ


# Subir nivel
# Devolvé una lista NUEVA de dicts con el "nivel" de cada uno sumado en `n` (sin tocar los
# originales).
def subir_nivel(pokes, n):
    """Devolvé los pokes con el nivel subido en n."""
    # TU CÓDIGO ACÁ


# Contar por tipo
# Devolvé un dict tipo → cantidad de pokes de ese tipo.
def contar_por_tipo(pokes):
    """Devolvé un dict tipo → cantidad."""
    # TU CÓDIGO ACÁ


# Nombres filtrados
# Devolvé los NOMBRES de los pokes con nivel mayor o igual a `minimo`.
def nombres_filtrados(pokes, minimo):
    """Devolvé los nombres con nivel >= minimo."""
    # TU CÓDIGO ACÁ


# ¿Existe? (ignorando mayúsculas y espacios)
# Devolvé True si hay un poke cuyo nombre, normalizado, coincida con `nombre` normalizado.
# Ejemplo:  existe([{"nombre": "Pikachu", ...}], "  pikachu ")  →  True
def existe(pokes, nombre):
    """Devolvé True si está ese nombre (normalizado)."""
    # TU CÓDIGO ACÁ


# Buscar (ignorando mayúsculas y espacios)
# Devolvé el dict del poke cuyo nombre normalizado coincida con `nombre`, o None.
def buscar(pokes, nombre):
    """Devolvé el poke con ese nombre, o None."""
    # TU CÓDIGO ACÁ


# Nivel total
# Devolvé la suma de los niveles.
def nivel_total(pokes):
    """Devolvé la suma de los niveles."""
    # TU CÓDIGO ACÁ


# Mapear nombres
# Aplicá `func` al "nombre" de cada poke y devolvé la lista de resultados.
# Ejemplo:  mapear_nombres([{"nombre": "abc"}], str.upper)  →  ["ABC"]
def mapear_nombres(pokes, func):
    """Devolvé func aplicada a cada nombre."""
    # TU CÓDIGO ACÁ


# Agregar slug
# Devolvé una lista NUEVA de dicts, cada uno con una clave extra "slug" igual al nombre
# normalizado (sin espacios, en minúsculas).
def agregar_slug(pokes):
    """Devolvé los pokes con una clave 'slug'."""
    # TU CÓDIGO ACÁ
