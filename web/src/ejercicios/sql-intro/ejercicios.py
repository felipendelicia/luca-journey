"""
✏️ Ejercicios — SQL: leer datos

Una base de datos guarda info en TABLAS (filas y columnas), como un Excel.
Cada función recibe una conexión a una base con la tabla 'pokemon'
(columnas: nombre, nivel, tipo). Vos escribís el SQL para leer lo que se pide.
"""
import sqlite3


# 1) Devolvé los NOMBRES de todos los Pokémon. Usá SELECT.
def todos(conexion):
    """Devolvé una lista con los nombres (SELECT nombre FROM pokemon)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Devolvé CUÁNTOS Pokémon hay. Usá SELECT COUNT(*).
def cuantos(conexion):
    """Devolvé un número entero. Pista: .fetchone()[0]."""
    # TU CÓDIGO ACÁ
    pass


# 3) Devolvé la lista de NIVELES (la columna 'nivel').
def niveles(conexion):
    """Devolvé una lista de enteros."""
    # TU CÓDIGO ACÁ
    pass


# 4) Devolvé pares (nombre, nivel) de cada Pokémon.
def nombres_y_niveles(conexion):
    """Devolvé una lista de tuplas (nombre, nivel). Pista: SELECT nombre, nivel ..."""
    # TU CÓDIGO ACÁ
    pass


# 5) Devolvé el nombre del PRIMER Pokémon de la tabla. Usá LIMIT 1.
def primero(conexion):
    """Devolvé un string (el nombre). Pista: .fetchone()[0]."""
    # TU CÓDIGO ACÁ
    pass
