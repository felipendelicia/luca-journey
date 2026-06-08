"""✅ Soluciones — SQL: leer datos"""
import sqlite3


def todos(conexion):
    return [fila[0] for fila in conexion.execute("SELECT nombre FROM pokemon")]


def cuantos(conexion):
    return conexion.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]


def niveles(conexion):
    return [fila[0] for fila in conexion.execute("SELECT nivel FROM pokemon")]


def nombres_y_niveles(conexion):
    return [(fila[0], fila[1]) for fila in conexion.execute("SELECT nombre, nivel FROM pokemon")]


def primero(conexion):
    return conexion.execute("SELECT nombre FROM pokemon LIMIT 1").fetchone()[0]


def ordenados_por_nivel(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC").fetchall()]


def mas_de(conexion, n):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE nivel > ?", (n,)).fetchall()]


def de_tipo(conexion, tipo):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE tipo = ?", (tipo,)).fetchall()]


def promedio_nivel(conexion):
    return conexion.execute("SELECT AVG(nivel) FROM pokemon").fetchone()[0]


def maximo_nivel(conexion):
    return conexion.execute("SELECT MAX(nivel) FROM pokemon").fetchone()[0]


def minimo_nivel(conexion):
    return conexion.execute("SELECT MIN(nivel) FROM pokemon").fetchone()[0]


def nivel_total(conexion):
    return conexion.execute("SELECT SUM(nivel) FROM pokemon").fetchone()[0]


def contar_de_tipo(conexion, tipo):
    return conexion.execute("SELECT COUNT(*) FROM pokemon WHERE tipo = ?", (tipo,)).fetchone()[0]


def el_mas_fuerte(conexion):
    return conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC LIMIT 1").fetchone()[0]


def tipos_distintos(conexion):
    return [f[0] for f in conexion.execute("SELECT DISTINCT tipo FROM pokemon ORDER BY tipo").fetchall()]


def existe(conexion, nombre):
    return conexion.execute("SELECT 1 FROM pokemon WHERE nombre = ?", (nombre,)).fetchone() is not None


def nivel_de(conexion, nombre):
    fila = conexion.execute("SELECT nivel FROM pokemon WHERE nombre = ?", (nombre,)).fetchone()
    return fila[0] if fila else None


def primeros(conexion, n):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon LIMIT ?", (n,)).fetchall()]


def nombres_que_empiezan(conexion, letra):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE nombre LIKE ?", (letra + "%",)).fetchall()]


def ordenados_alfabeticamente(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY nombre").fetchall()]
