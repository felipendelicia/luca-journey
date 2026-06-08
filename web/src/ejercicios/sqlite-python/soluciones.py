"""✅ Soluciones — SQLite desde Python"""
import sqlite3


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


def todos(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon").fetchall()]


def niveles(conexion):
    return [f[0] for f in conexion.execute("SELECT nivel FROM pokemon").fetchall()]


def actualizar(conexion, nombre, nivel):
    conexion.execute("UPDATE pokemon SET nivel = ? WHERE nombre = ?", (nivel, nombre))
    conexion.commit()


def borrar(conexion, nombre):
    conexion.execute("DELETE FROM pokemon WHERE nombre = ?", (nombre,))
    conexion.commit()


def existe(conexion, nombre):
    return conexion.execute("SELECT 1 FROM pokemon WHERE nombre = ?", (nombre,)).fetchone() is not None


def nivel_de(conexion, nombre):
    fila = conexion.execute("SELECT nivel FROM pokemon WHERE nombre = ?", (nombre,)).fetchone()
    return fila[0] if fila else None


def promedio(conexion):
    return conexion.execute("SELECT AVG(nivel) FROM pokemon").fetchone()[0]


def maximo(conexion):
    return conexion.execute("SELECT MAX(nivel) FROM pokemon").fetchone()[0]


def guardar_varios(conexion, filas):
    conexion.executemany("INSERT INTO pokemon VALUES (?, ?)", filas)
    conexion.commit()


def mas_fuerte(conexion):
    return conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC LIMIT 1").fetchone()[0]


def ordenados(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC").fetchall()]


def contar_arriba(conexion, n):
    return conexion.execute("SELECT COUNT(*) FROM pokemon WHERE nivel > ?", (n,)).fetchone()[0]


def vaciar(conexion):
    conexion.execute("DELETE FROM pokemon")
    conexion.commit()


def a_diccionario(conexion):
    return {f[0]: f[1] for f in conexion.execute("SELECT nombre, nivel FROM pokemon").fetchall()}


def subir_nivel(conexion, nombre, cuanto):
    conexion.execute("UPDATE pokemon SET nivel = nivel + ? WHERE nombre = ?", (cuanto, nombre))
    conexion.commit()


def total_niveles(conexion):
    return conexion.execute("SELECT SUM(nivel) FROM pokemon").fetchone()[0]
