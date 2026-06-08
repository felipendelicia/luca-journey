"""✏️ Ejercicios — Consumir una API

Cuando tu programa le pide datos a una API (ej: la PokéAPI), recibe JSON. Acá practicás
PROCESAR esas respuestas (extraer, filtrar, manejar errores). Te pasamos la respuesta
ya como texto JSON. ✅ Corregir al terminar.
"""
import json


# Extraer los tipos
# La respuesta es {"name": "pikachu", "tipos": ["electrico"]}. Devolvé la lista de 'tipos'.
# Ejemplo:  extraer_tipos('{"name": "vulpix", "tipos": ["fuego"]}')  →  ["fuego"]
def extraer_tipos(texto):
    """Devolvé la lista de la clave 'tipos'."""
    # TU CÓDIGO ACÁ
    pass


# Nombre y nivel (tupla)
# A partir de {"nombre": .., "nivel": ..}, devolvé la tupla (nombre, nivel).
# Ejemplo:  nombre_y_nivel('{"nombre": "Pikachu", "nivel": 25}')  →  ("Pikachu", 25)
def nombre_y_nivel(texto):
    """Devolvé (nombre, nivel)."""
    # TU CÓDIGO ACÁ
    pass


# Filtrar por tipo
# La respuesta es una LISTA de Pokémon (cada uno con 'nombre' y 'tipo'). Devolvé los
# NOMBRES de los que sean del 'tipo' pedido.
# Ejemplo:  filtrar_por_tipo('[{"nombre":"Vulpix","tipo":"Fuego"}]', "Fuego")  →  ["Vulpix"]
def filtrar_por_tipo(texto, tipo):
    """Devolvé los nombres de los Pokémon de ese 'tipo'."""
    # TU CÓDIGO ACÁ
    pass


# Manejar la respuesta
# Si el status es 200, devolvé los datos (json.loads(texto)). Si no, devolvé None.
# Ejemplo:  manejar_respuesta(200, '{"ok": 1}')  →  {"ok": 1}   ·   manejar_respuesta(404, "...")  →  None
def manejar_respuesta(status, texto):
    """Parseá solo si status == 200; si no, devolvé None."""
    # TU CÓDIGO ACÁ
    pass


# Contar resultados
# La respuesta es {"results": [...]}. Devolvé cuántos resultados hay.
# Ejemplo:  contar_resultados('{"results": [1, 2, 3]}')  →  3
def contar_resultados(texto):
    """Devolvé la cantidad de elementos en 'results'."""
    # TU CÓDIGO ACÁ
    pass


# El primer resultado
# La respuesta es {"results": [{"name": ..}, ...]}. Devolvé el 'name' del primero.
# Ejemplo:  primer_resultado('{"results": [{"name": "pikachu"}]}')  →  "pikachu"
def primer_resultado(texto):
    """Devolvé el 'name' del primer elemento de 'results'."""
    # TU CÓDIGO ACÁ
    pass


# Último resultado
# La respuesta es un JSON de una lista de Pokémon (dicts). Devolvé el último, o None si vacía.
def ultimo_resultado(texto):
    """Devolvé el último Pokémon, o None."""
    # TU CÓDIGO ACÁ
    pass


# Nombres
# Devolvé la lista de "nombre" de cada Pokémon.
def nombres_de(texto):
    """Devolvé los nombres."""
    # TU CÓDIGO ACÁ
    pass


# Ordenar por nivel
# Devolvé los NOMBRES ordenados de mayor a menor "nivel".
def ordenar_por_nivel(texto):
    """Devolvé los nombres ordenados por nivel (desc)."""
    # TU CÓDIGO ACÁ
    pass


# Promedio de nivel
# Devolvé el promedio de los niveles.
def promedio_nivel(texto):
    """Devolvé el nivel promedio."""
    # TU CÓDIGO ACÁ
    pass


# El más fuerte
# Devolvé el "nombre" del Pokémon de mayor nivel.
def mas_fuerte(texto):
    """Devolvé el nombre del de mayor nivel."""
    # TU CÓDIGO ACÁ
    pass


# ¿Existe?
# Devolvé True si hay un Pokémon con ese "nombre".
def existe(texto, nombre):
    """Devolvé True si está ese nombre."""
    # TU CÓDIGO ACÁ
    pass


# Buscar
# Devolvé el dict del Pokémon con ese "nombre", o None si no está.
def buscar(texto, nombre):
    """Devolvé el Pokémon con ese nombre, o None."""
    # TU CÓDIGO ACÁ
    pass


# Tipos únicos
# Devolvé una lista ORDENADA con los tipos distintos.
def tipos_unicos(texto):
    """Devolvé los tipos distintos, ordenados."""
    # TU CÓDIGO ACÁ
    pass


# Contar por tipo
# Devolvé un dict tipo → cantidad.
def contar_por_tipo(texto):
    """Devolvé un dict tipo → cantidad."""
    # TU CÓDIGO ACÁ
    pass


# Filtrar por nivel mínimo
# Devolvé los NOMBRES de los Pokémon con nivel mayor o igual a `minimo`.
def filtrar_nivel_minimo(texto, minimo):
    """Devolvé los nombres con nivel >= minimo."""
    # TU CÓDIGO ACÁ
    pass


# ¿Hay resultados?
# Devolvé True si la lista tiene al menos un Pokémon.
def hay_resultados(texto):
    """Devolvé True si hay resultados."""
    # TU CÓDIGO ACÁ
    pass


# Nombres de un tipo
# Devolvé los NOMBRES de los Pokémon cuyo "tipo" sea `tipo`.
def nombres_de_tipo(texto, tipo):
    """Devolvé los nombres de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Nivel de un Pokémon
# Devolvé el "nivel" del Pokémon con ese "nombre", o None.
def nivel_de(texto, nombre):
    """Devolvé el nivel de ese Pokémon, o None."""
    # TU CÓDIGO ACÁ
    pass


# Resumen
# Devolvé un dict con "total" (cantidad) y "tipos" (cantidad de tipos distintos).
def resumen(texto):
    """Devolvé un dict resumen."""
    # TU CÓDIGO ACÁ
    pass
