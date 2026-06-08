"""✅ Soluciones — SQL: agregaciones y GROUP BY"""
import sqlite3


def total(conexion):
    return conexion.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]


def nivel_promedio(conexion):
    return conexion.execute("SELECT AVG(nivel) FROM pokemon").fetchone()[0]


def nivel_maximo(conexion):
    return conexion.execute("SELECT MAX(nivel) FROM pokemon").fetchone()[0]


def suma_niveles(conexion):
    return conexion.execute("SELECT SUM(nivel) FROM pokemon").fetchone()[0]


def cuantos_por_tipo(conexion):
    filas = conexion.execute("SELECT tipo, COUNT(*) FROM pokemon GROUP BY tipo")
    return {tipo: cant for tipo, cant in filas}


def promedio_por_tipo(conexion):
    filas = conexion.execute("SELECT tipo, AVG(nivel) FROM pokemon GROUP BY tipo")
    return {tipo: prom for tipo, prom in filas}


def nivel_minimo(conexion):
    return conexion.execute("SELECT MIN(nivel) FROM pokemon").fetchone()[0]


def cuantos_de_tipo(conexion, tipo):
    return conexion.execute("SELECT COUNT(*) FROM pokemon WHERE tipo = ?", (tipo,)).fetchone()[0]


def suma_por_tipo(conexion):
    return {f[0]: f[1] for f in conexion.execute("SELECT tipo, SUM(nivel) FROM pokemon GROUP BY tipo").fetchall()}


def maximo_por_tipo(conexion):
    return {f[0]: f[1] for f in conexion.execute("SELECT tipo, MAX(nivel) FROM pokemon GROUP BY tipo").fetchall()}


def tipo_mas_numeroso(conexion):
    return conexion.execute("SELECT tipo FROM pokemon GROUP BY tipo ORDER BY COUNT(*) DESC LIMIT 1").fetchone()[0]


def nivel_total_de_tipo(conexion, tipo):
    return conexion.execute("SELECT SUM(nivel) FROM pokemon WHERE tipo = ?", (tipo,)).fetchone()[0]


def cantidad_tipos(conexion):
    return conexion.execute("SELECT COUNT(DISTINCT tipo) FROM pokemon").fetchone()[0]


def rango_nivel(conexion):
    return conexion.execute("SELECT MAX(nivel) - MIN(nivel) FROM pokemon").fetchone()[0]


def cuantos_arriba_de(conexion, n):
    return conexion.execute("SELECT COUNT(*) FROM pokemon WHERE nivel > ?", (n,)).fetchone()[0]


def promedio_de_tipo(conexion, tipo):
    return conexion.execute("SELECT AVG(nivel) FROM pokemon WHERE tipo = ?", (tipo,)).fetchone()[0]


def minimo_por_tipo(conexion):
    return {f[0]: f[1] for f in conexion.execute("SELECT tipo, MIN(nivel) FROM pokemon GROUP BY tipo").fetchall()}


def el_mas_fuerte(conexion):
    return conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC LIMIT 1").fetchone()[0]


def hay_de_tipo(conexion, tipo):
    return conexion.execute("SELECT COUNT(*) FROM pokemon WHERE tipo = ?", (tipo,)).fetchone()[0] > 0


def conteo_por_tipo_ordenado(conexion):
    return [(f[0], f[1]) for f in conexion.execute("SELECT tipo, COUNT(*) FROM pokemon GROUP BY tipo ORDER BY COUNT(*) DESC, tipo").fetchall()]
