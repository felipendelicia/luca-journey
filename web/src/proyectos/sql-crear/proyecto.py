# Líder Gardenia — Vivero Pokémon (solución de referencia).
# El preamble (conexion vacía) está en meta.json y se antepone al corregir.

def crear_tabla(conexion):
    conexion.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT, nivel INTEGER)")

def insertar_uno(conexion, nombre, tipo, nivel):
    conexion.execute("INSERT INTO pokemon VALUES (?, ?, ?)", (nombre, tipo, nivel))

def insertar_varios(conexion, filas):
    conexion.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", filas)

def contar_registros(conexion):
    return conexion.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]
