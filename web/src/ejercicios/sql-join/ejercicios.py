"""✏️ Ejercicios — SQL: relaciones y JOIN

Los datos suelen estar en VARIAS tablas relacionadas. JOIN las combina. Tenés dos tablas:
  pokemon(nombre, tipo)  ·  tipos(tipo, debilidad)   (relacionadas por 'tipo')
✅ Corregir al terminar.
"""
import sqlite3


# Combinar con JOIN
# Devolvé pares (nombre, debilidad) combinando ambas tablas.
# Pista: SELECT p.nombre, t.debilidad FROM pokemon p JOIN tipos t ON p.tipo = t.tipo.
# Ejemplo:  [("Charizard", "Agua"), ("Blastoise", "Planta")]
def con_debilidad(conexion):
    """Devolvé una lista de tuplas (nombre, debilidad)."""
    # TU CÓDIGO ACÁ
    pass


# Debilidad de uno
# Devolvé la debilidad de UN Pokémon (por su nombre). Usá JOIN + WHERE.
# Ejemplo:  debilidad_de(con, "Charizard")  →  "Agua"
def debilidad_de(conexion, nombre):
    """Devolvé la debilidad del tipo de ese Pokémon (str)."""
    # TU CÓDIGO ACÁ
    pass


# Débiles a un elemento
# Devolvé los NOMBRES de los Pokémon cuyo tipo es débil a 'elemento'.
# Pista: JOIN + WHERE t.debilidad = ?.
# Ejemplo:  debiles_a(con, "Agua")  →  ["Charizard", "Vulpix"]
def debiles_a(conexion, elemento):
    """Devolvé los nombres de los débiles a 'elemento'."""
    # TU CÓDIGO ACÁ
    pass


# Nombre y debilidad (JOIN)
# Devolvé pares (nombre, debilidad) uniendo pokemon con tipos por la columna 'tipo'.
# Pista: SELECT p.nombre, t.debilidad FROM pokemon p JOIN tipos t ON p.tipo = t.tipo.
def nombres_y_debilidad(conexion):
    """Devolvé (nombre, debilidad) con un JOIN."""
    # TU CÓDIGO ACÁ
    pass


# Cuántos débiles a un elemento
# Devolvé cuántos Pokémon son débiles al elemento `elemento` (su tipo tiene esa debilidad).
def cuantos_debiles_a(conexion, elemento):
    """Devolvé cuántos son débiles a ese elemento."""
    # TU CÓDIGO ACÁ
    pass


# Tipos con su debilidad
# Devolvé pares (tipo, debilidad) de la tabla tipos.
def tipos_con_debilidad(conexion):
    """Devolvé (tipo, debilidad) de la tabla tipos."""
    # TU CÓDIGO ACÁ
    pass


# Debilidad de un tipo
# Devolvé la debilidad del tipo `tipo`, o None si no está en la tabla tipos.
def debilidad_del_tipo(conexion, tipo):
    """Devolvé la debilidad de ese tipo, o None."""
    # TU CÓDIGO ACÁ
    pass


# Sin debilidad conocida
# Devolvé los NOMBRES de los Pokémon cuyo tipo NO está en la tabla tipos.
# Pista: WHERE tipo NOT IN (SELECT tipo FROM tipos).
def sin_debilidad_conocida(conexion):
    """Devolvé los nombres sin debilidad conocida."""
    # TU CÓDIGO ACÁ
    pass


# Con debilidad conocida
# Devolvé los NOMBRES de los Pokémon cuyo tipo SÍ está en la tabla tipos.
def con_debilidad_conocida(conexion):
    """Devolvé los nombres con debilidad conocida."""
    # TU CÓDIGO ACÁ
    pass


# Contar el JOIN
# Devolvé cuántas filas tiene el JOIN entre pokemon y tipos.
def contar_join(conexion):
    """Devolvé la cantidad de filas del JOIN."""
    # TU CÓDIGO ACÁ
    pass


# Mapa de debilidades
# Devolvé un dict tipo → debilidad (de la tabla tipos).
def mapa_debilidades(conexion):
    """Devolvé un dict tipo → debilidad."""
    # TU CÓDIGO ACÁ
    pass


# Tipos de los Pokémon
# Devolvé los tipos DISTINTOS que aparecen en la tabla pokemon, ordenados.
def tipos_de_pokemon(conexion):
    """Devolvé los tipos distintos de pokemon, ordenados."""
    # TU CÓDIGO ACÁ
    pass


# Debilidades distintas
# Devolvé las debilidades DISTINTAS de la tabla tipos, ordenadas.
def debilidades_distintas(conexion):
    """Devolvé las debilidades distintas, ordenadas."""
    # TU CÓDIGO ACÁ
    pass


# Nombre, tipo y debilidad
# Devolvé tuplas (nombre, tipo, debilidad) con el JOIN.
def nombre_tipo_debilidad(conexion):
    """Devolvé (nombre, tipo, debilidad)."""
    # TU CÓDIGO ACÁ
    pass


# ¿Hay debilidad para ese tipo?
# Devolvé True si el tipo `tipo` está en la tabla tipos.
def hay_debilidad_para(conexion, tipo):
    """Devolvé True si hay debilidad para ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Primer débil a un elemento
# Devolvé el NOMBRE del primer Pokémon débil a `elemento`, o None.
def primer_debil_a(conexion, elemento):
    """Devolvé el primer débil a ese elemento, o None."""
    # TU CÓDIGO ACÁ
    pass


# Tipos que pierden contra
# Devolvé los TIPOS cuya debilidad sea `elemento`.
def tipos_que_pierden_contra(conexion, elemento):
    """Devolvé los tipos débiles a ese elemento."""
    # TU CÓDIGO ACÁ
    pass


# Cuántos de un tipo
# Devolvé cuántos Pokémon hay de tipo `tipo`.
def cuantos_de_tipo(conexion, tipo):
    """Devolvé cuántos son de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Nombres débiles ordenados
# Devolvé los NOMBRES de los Pokémon con debilidad conocida, ordenados alfabéticamente (con JOIN).
def nombres_debiles_ordenados(conexion):
    """Devolvé los nombres con debilidad, ordenados."""
    # TU CÓDIGO ACÁ
    pass


# Todos los nombres
# Devolvé los NOMBRES de todos los Pokémon.
def todos_los_nombres(conexion):
    """Devolvé todos los nombres."""
    # TU CÓDIGO ACÁ
    pass
