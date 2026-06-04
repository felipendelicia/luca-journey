"""
✏️ Ejercicios — Proyecto: Pokédex en SQLite

Tu Pokédex guardada en una base de datos. Junta todo Sinnoh: crear, insertar,
consultar, agrupar — desde Python. Tabla 'pokemon' (nombre, tipo, nivel).
"""
import sqlite3


# 1) Creá la base con la tabla 'pokemon' (nombre TEXT, tipo TEXT, nivel INTEGER)
#    y devolvé la conexión.
def crear_pokedex():
    """Devolvé una conexión con la tabla 'pokemon' lista."""
    # TU CÓDIGO ACÁ
    pass


# 2) Agregá un Pokémon y confirmá (commit).
def agregar(conexion, nombre, tipo, nivel):
    """INSERT con parámetros + commit."""
    # TU CÓDIGO ACÁ
    pass


# 3) Devolvé los nombres de todos, ordenados alfabéticamente.
def listar(conexion):
    """SELECT nombre ... ORDER BY nombre. Devolvé una lista."""
    # TU CÓDIGO ACÁ
    pass


# 4) Devolvé los nombres de un tipo dado.
def por_tipo(conexion, tipo):
    """WHERE tipo = ?. Devolvé una lista de nombres."""
    # TU CÓDIGO ACÁ
    pass


# 5) Devolvé el NOMBRE del Pokémon de mayor nivel.
def el_mas_fuerte(conexion):
    """ORDER BY nivel DESC LIMIT 1 -> .fetchone()[0]."""
    # TU CÓDIGO ACÁ
    pass


# 6) ¿Cuántos hay de cada tipo? Devolvé un dict {tipo: cantidad}.
def cuantos_por_tipo(conexion):
    """GROUP BY tipo."""
    # TU CÓDIGO ACÁ
    pass
