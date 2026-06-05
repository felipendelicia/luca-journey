# Líder Volkner — Mini Pokédex en SQLite (solución de referencia).
# El preamble (import sqlite3) está en meta.json y se antepone al corregir.

def crear_pokedex():
    conexion = sqlite3.connect(":memory:")
    conexion.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT, nivel INTEGER)")
    return conexion

def agregar(conexion, nombre, tipo, nivel):
    conexion.execute("INSERT INTO pokemon VALUES (?, ?, ?)", (nombre, tipo, nivel))
    conexion.commit()

def listar(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY nombre")]

def por_tipo(conexion, tipo):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE tipo = ?", (tipo,))]

def el_mas_fuerte(conexion):
    return conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC LIMIT 1").fetchone()[0]

def actualizar_nivel(conexion, nombre, nuevo_nivel):
    conexion.execute("UPDATE pokemon SET nivel = ? WHERE nombre = ?", (nuevo_nivel, nombre))

def borrar(conexion, nombre):
    conexion.execute("DELETE FROM pokemon WHERE nombre = ?", (nombre,))
