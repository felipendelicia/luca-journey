"""🔶 Ejercicios — Algoritmos sobre la Pokédex

Juntás búsqueda, orden y conteo sobre una lista de Pokémon (cada uno un dict con
"nombre", "tipo" y "nivel"). ✅ Corregí cuando termines.
"""


# Contar por tipo
# Devolvé un dict tipo → cantidad de Pokémon de ese tipo.
# Ejemplo:  contar_tipos([{"nombre": "a", "tipo": "agua"}, {"nombre": "b", "tipo": "agua"}])
#               →  {"agua": 2}
def contar_tipos(pokes):
    """Devolvé un dict tipo → cantidad."""


# Ordenar por nivel
# Devolvé la lista de Pokémon ordenada por nivel de MAYOR a menor.
# Ejemplo:  ordenar_por_nivel([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}])
#               →  [{"nombre": "b", "nivel": 20}, {"nombre": "a", "nivel": 5}]
def ordenar_por_nivel(pokes):
    """Devolvé los pokes ordenados por nivel descendente."""


# Buscar por nombre
# Devolvé el primer Pokémon cuyo "nombre" coincida, o None si no está.
# Ejemplo:  buscar([{"nombre": "Pikachu"}], "Pikachu")  →  {"nombre": "Pikachu"}
def buscar(pokes, nombre):
    """Devolvé el primer poke con ese nombre, o None."""


# Top N
# Devolvé los NOMBRES de los `n` Pokémon de mayor nivel, de mayor a menor.
# Ejemplo:  top_n([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}, {"nombre": "c", "nivel": 12}], 2)
#               →  ["b", "c"]
def top_n(pokes, n):
    """Devolvé los nombres de los n de mayor nivel."""


# Promedio de nivel
# Devolvé el promedio de los niveles.  Ejemplo:  niveles 20 y 12  →  promedio_nivel(pokes)  →  16.0
def promedio_nivel(pokes):
    """Devolvé el nivel promedio."""
    # TU CÓDIGO ACÁ


# Nivel máximo
# Devolvé el nivel más alto del grupo.
def nivel_maximo(pokes):
    """Devolvé el nivel máximo."""
    # TU CÓDIGO ACÁ


# El más fuerte
# Devolvé el DICCIONARIO del Pokémon de mayor nivel.
def el_mas_fuerte(pokes):
    """Devolvé el Pokémon de mayor nivel."""
    # TU CÓDIGO ACÁ


# Filtrar por tipo
# Devolvé la lista de Pokémon (los dicts) cuyo "tipo" sea `tipo`.
def filtrar_por_tipo(pokes, tipo):
    """Devolvé los Pokémon de ese tipo."""
    # TU CÓDIGO ACÁ


# Nombres
# Devolvé una lista con el "nombre" de cada Pokémon.
def nombres(pokes):
    """Devolvé la lista de nombres."""
    # TU CÓDIGO ACÁ


# Tipos únicos
# Devolvé una lista ORDENADA con los tipos distintos.
def tipos_unicos(pokes):
    """Devolvé los tipos distintos, ordenados."""
    # TU CÓDIGO ACÁ


# ¿Existe?
# Devolvé True si hay un Pokémon con ese "nombre".
def existe(pokes, nombre):
    """Devolvé True si está ese nombre."""
    # TU CÓDIGO ACÁ


# Nivel de uno
# Devolvé el "nivel" del Pokémon con ese nombre, o None si no está.
def nivel_de(pokes, nombre):
    """Devolvé el nivel de ese Pokémon, o None."""
    # TU CÓDIGO ACÁ


# Subir nivel a todos
# Devolvé una lista NUEVA de dicts, con el "nivel" de cada uno sumado en `n` (no modifiques
# los originales).
def subir_nivel_todos(pokes, n):
    """Devolvé los Pokémon con el nivel subido en n."""
    # TU CÓDIGO ACÁ


# Más de cierto nivel
# Devolvé los Pokémon cuyo nivel sea ESTRICTAMENTE mayor que `n`.
def mas_de_nivel(pokes, n):
    """Devolvé los Pokémon de nivel mayor a n."""
    # TU CÓDIGO ACÁ


# Agrupar por tipo
# Devolvé un dict tipo → lista de NOMBRES de ese tipo (en orden de aparición).
# Ejemplo:  {"agua": ["staryu", "gyarados"], ...}
def agrupar_por_tipo(pokes):
    """Devolvé un dict tipo → lista de nombres."""
    # TU CÓDIGO ACÁ


# Ordenar por nombre
# Devolvé los NOMBRES ordenados alfabéticamente.
def ordenar_por_nombre(pokes):
    """Devolvé los nombres ordenados alfabéticamente."""
    # TU CÓDIGO ACÁ


# El tipo más común
# Devolvé el "tipo" que más se repite.
def tipo_mas_comun(pokes):
    """Devolvé el tipo más frecuente."""
    # TU CÓDIGO ACÁ


# Nivel total
# Devolvé la suma de los niveles de todos.
def nivel_total(pokes):
    """Devolvé la suma de los niveles."""
    # TU CÓDIGO ACÁ


# ¿Equipo balanceado?
# Devolvé True si todos los Pokémon son de tipos distintos (ninguno repetido).
def equipo_balanceado(pokes):
    """Devolvé True si no hay tipos repetidos."""
    # TU CÓDIGO ACÁ


# Cuántos hay
# Devolvé cuántos Pokémon tiene la lista.
def contar(pokes):
    """Devolvé la cantidad de Pokémon."""
    # TU CÓDIGO ACÁ
