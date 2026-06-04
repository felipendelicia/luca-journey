"""
✏️ Ejercicios — SQLite desde Python

Hasta ahora escribiste SQL. Acá lo manejás DESDE Python con el módulo sqlite3:
conectarte, ejecutar, traer resultados (fetchone/fetchall) y guardar (commit).
"""
import sqlite3


# 1) Creá una base en memoria con una tabla 'pokemon' (nombre TEXT, nivel INTEGER)
#    y devolvé la conexión. Pista: sqlite3.connect(":memory:").
def crear_conexion():
    """Devolvé una conexión con la tabla 'pokemon' ya creada."""
    # TU CÓDIGO ACÁ
    pass


# 2) Guardá un Pokémon en la tabla y confirmá con commit().
def guardar(conexion, nombre, nivel):
    """INSERT con parámetros (?), después conexion.commit()."""
    # TU CÓDIGO ACÁ
    pass


# 3) Devolvé cuántos Pokémon hay. Usá un cursor y fetchone().
def cantidad(conexion):
    """cur = conexion.cursor(); cur.execute(...); return cur.fetchone()[0]."""
    # TU CÓDIGO ACÁ
    pass


# 4) Buscá un Pokémon por nombre. Devolvé su fila (tupla) o None si no existe.
def buscar(conexion, nombre):
    """SELECT * ... WHERE nombre = ?  -> .fetchone()  (devuelve None si no hay)."""
    # TU CÓDIGO ACÁ
    pass
