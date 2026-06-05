# Líder Candice — Archivo del Hielo (solución de referencia).
# El preamble (import sqlite3) está en meta.json y se antepone al corregir.

def crear_conexion():
    conexion = sqlite3.connect(":memory:")
    conexion.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
    return conexion

def guardar(conexion, nombre, nivel):
    conexion.execute("INSERT INTO pokemon VALUES (?, ?)", (nombre, nivel))
    conexion.commit()

def cantidad(conexion):
    cur = conexion.cursor()
    cur.execute("SELECT COUNT(*) FROM pokemon")
    return cur.fetchone()[0]

def buscar(conexion, nombre):
    return conexion.execute("SELECT * FROM pokemon WHERE nombre = ?", (nombre,)).fetchone()
