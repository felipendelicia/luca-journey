"""✏️ Ejercicios — SQL: crear e insertar

Creamos tablas (CREATE TABLE) y metemos datos (INSERT). La conexión te llega vacía.
✅ Corregir al terminar.
"""
import sqlite3


# Crear una tabla
# Creá una tabla 'entrenadores' con columnas: nombre (TEXT) y medallas (INTEGER).
# Pista: conexion.execute("CREATE TABLE entrenadores (nombre TEXT, medallas INTEGER)").
def crear_tabla(conexion):
    """Creá la tabla 'entrenadores'."""
    # TU CÓDIGO ACÁ
    pass


# Insertar uno
# Insertá UN entrenador en la tabla (ya creada). Usá parámetros (?) por seguridad.
# Pista: conexion.execute("INSERT INTO entrenadores VALUES (?, ?)", (nombre, medallas)).
def insertar(conexion, nombre, medallas):
    """Insertá un entrenador (nombre, medallas)."""
    # TU CÓDIGO ACÁ
    pass


# Insertar varios
# Insertá VARIOS entrenadores de una. 'filas' es una lista de tuplas (nombre, medallas).
# Pista: conexion.executemany("INSERT INTO entrenadores VALUES (?, ?)", filas).
def insertar_varios(conexion, filas):
    """Insertá todas las filas de una."""
    # TU CÓDIGO ACÁ
    pass


# Crear + insertar
# Creá la tabla 'pokemon' (nombre TEXT, nivel INTEGER) e insertá a ('Pikachu', 25).
def crear_pokedex(conexion):
    """Creá la tabla y meté ('Pikachu', 25)."""
    # TU CÓDIGO ACÁ
    pass
