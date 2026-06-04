"""✏️ Ejercicios — Proyecto: Pokédex en SQLite

Tu Pokédex guardada en una base de datos. Junta todo Sinnoh: crear, insertar, consultar
y agrupar — desde Python. Tabla 'pokemon' (nombre, tipo, nivel). ✅ Corregir al terminar.
"""
import sqlite3


# Crear la Pokédex
# Creá la base con la tabla 'pokemon' (nombre TEXT, tipo TEXT, nivel INTEGER) y devolvé
# la conexión.
def crear_pokedex():
    """Devolvé una conexión con la tabla 'pokemon' lista."""
    # TU CÓDIGO ACÁ
    pass


# Agregar un Pokémon
# Insertá un Pokémon y confirmá (commit). Pista: INSERT con (?) + commit.
def agregar(conexion, nombre, tipo, nivel):
    """Insertá (nombre, tipo, nivel) y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# Listar (ordenado)
# Devolvé los nombres de todos, ordenados alfabéticamente. Pista: SELECT nombre ... ORDER BY nombre.
def listar(conexion):
    """Devolvé la lista de nombres ordenada."""
    # TU CÓDIGO ACÁ
    pass


# Por tipo
# Devolvé los nombres de un tipo dado. Pista: WHERE tipo = ?.
# Ejemplo:  por_tipo(con, "Fuego")  →  ["Charizard", "Vulpix"]
def por_tipo(conexion, tipo):
    """Devolvé los nombres de ese 'tipo'."""
    # TU CÓDIGO ACÁ
    pass


# El más fuerte
# Devolvé el NOMBRE del Pokémon de mayor nivel. Pista: ORDER BY nivel DESC LIMIT 1 → fetchone()[0].
def el_mas_fuerte(conexion):
    """Devolvé el nombre del de mayor nivel."""
    # TU CÓDIGO ACÁ
    pass


# Cuántos por tipo
# Devolvé un dict {tipo: cantidad}. Pista: SELECT tipo, COUNT(*) ... GROUP BY tipo.
# Ejemplo:  cuantos_por_tipo(con)  →  {"Fuego": 2, "Electrico": 1}
def cuantos_por_tipo(conexion):
    """Devolvé un dict {tipo: cantidad}."""
    # TU CÓDIGO ACÁ
    pass
