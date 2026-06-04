"""
✏️ Ejercicios — SQL: crear e insertar

Creamos tablas (CREATE TABLE) y metemos datos (INSERT). La conexión te llega vacía.
"""
import sqlite3


# 1) Creá una tabla 'entrenadores' con columnas: nombre (TEXT) y medallas (INTEGER).
def crear_tabla(conexion):
    """Ejecutá un CREATE TABLE entrenadores (nombre TEXT, medallas INTEGER)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Insertá UN entrenador en la tabla 'entrenadores' (ya creada).
def insertar(conexion, nombre, medallas):
    """INSERT INTO entrenadores VALUES (?, ?). Usá parámetros (?) por seguridad."""
    # TU CÓDIGO ACÁ
    pass


# 3) Insertá VARIOS entrenadores de una. 'filas' es una lista de tuplas (nombre, medallas).
def insertar_varios(conexion, filas):
    """Usá conexion.executemany(...)."""
    # TU CÓDIGO ACÁ
    pass


# 4) Creá la tabla 'pokemon' (nombre TEXT, nivel INTEGER) e insertá a Pikachu nivel 25.
def crear_pokedex(conexion):
    """Creá la tabla y meté un Pokémon: ('Pikachu', 25)."""
    # TU CÓDIGO ACÁ
    pass
