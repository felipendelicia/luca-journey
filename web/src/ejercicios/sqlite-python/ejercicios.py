"""✏️ Ejercicios — SQLite desde Python

Hasta ahora escribiste SQL. Acá lo manejás DESDE Python con el módulo sqlite3:
conectarte, ejecutar, traer resultados (fetchone/fetchall) y guardar (commit).
✅ Corregir al terminar.
"""
import sqlite3


# Crear la conexión
# Creá una base en memoria con una tabla 'pokemon' (nombre TEXT, nivel INTEGER) y
# devolvé la conexión. Pista: sqlite3.connect(":memory:") y un CREATE TABLE.
def crear_conexion():
    """Devolvé una conexión con la tabla 'pokemon' ya creada."""
    # TU CÓDIGO ACÁ
    pass


# Guardar con commit
# Insertá un Pokémon en la tabla y confirmá con commit(). Pista: INSERT con (?) + conexion.commit().
def guardar(conexion, nombre, nivel):
    """Insertá (nombre, nivel) y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# Contar con cursor
# Devolvé cuántos Pokémon hay, usando un cursor y fetchone().
# Pista: cur = conexion.cursor(); cur.execute("SELECT COUNT(*) ..."); return cur.fetchone()[0].
def cantidad(conexion):
    """Devolvé la cantidad de Pokémon (int)."""
    # TU CÓDIGO ACÁ
    pass


# Buscar uno (o None)
# Buscá un Pokémon por nombre. Devolvé su fila (tupla) o None si no existe.
# Pista: SELECT * ... WHERE nombre = ?  →  .fetchone()  (devuelve None si no hay).
# Ejemplo:  buscar(con, "Eevee")  →  ("Eevee", 15)   ·   buscar(con, "Mew")  →  None
def buscar(conexion, nombre):
    """Devolvé la fila del Pokémon, o None."""
    # TU CÓDIGO ACÁ
    pass
