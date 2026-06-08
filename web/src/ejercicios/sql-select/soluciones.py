"""✅ Soluciones — SQL: filtrar y ordenar"""
import sqlite3


def de_tipo(conexion, tipo):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE tipo = ?", (tipo,))]


def fuertes(conexion, minimo):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE nivel >= ? ORDER BY nivel DESC", (minimo,))]


def ordenados_por_nivel(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC")]


def empiezan_con(conexion, letra):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE nombre LIKE ?", (letra + "%",))]


def top(conexion, n):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC LIMIT ?", (n,))]


def debiles(conexion, maximo):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE nivel <= ?", (maximo,)).fetchall()]


def entre_niveles(conexion, lo, hi):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE nivel BETWEEN ? AND ?", (lo, hi)).fetchall()]


def no_de_tipo(conexion, tipo):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE tipo != ?", (tipo,)).fetchall()]


def contienen(conexion, sub):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE nombre LIKE ?", ("%" + sub + "%",)).fetchall()]


def ordenados_alfabeticamente(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY nombre").fetchall()]


def ultimo_alfabetico(conexion):
    return conexion.execute("SELECT nombre FROM pokemon ORDER BY nombre DESC LIMIT 1").fetchone()[0]


def nombres_y_tipos(conexion):
    return [(f[0], f[1]) for f in conexion.execute("SELECT nombre, tipo FROM pokemon").fetchall()]


def dos_tipos(conexion, t1, t2):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE tipo IN (?, ?)", (t1, t2)).fetchall()]


def cantidad_por_encima(conexion, n):
    return conexion.execute("SELECT COUNT(*) FROM pokemon WHERE nivel > ?", (n,)).fetchone()[0]


def nombres_largos(conexion, largo):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE LENGTH(nombre) > ?", (largo,)).fetchall()]


def el_de_nivel(conexion, nivel):
    fila = conexion.execute("SELECT nombre FROM pokemon WHERE nivel = ?", (nivel,)).fetchone()
    return fila[0] if fila else None


def distintos_tipos(conexion):
    return [f[0] for f in conexion.execute("SELECT DISTINCT tipo FROM pokemon ORDER BY tipo").fetchall()]


def los_n_mas_debiles(conexion, n):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel ASC LIMIT ?", (n,)).fetchall()]


def mas_fuerte_de_tipo(conexion, tipo):
    fila = conexion.execute("SELECT nombre FROM pokemon WHERE tipo = ? ORDER BY nivel DESC LIMIT 1", (tipo,)).fetchone()
    return fila[0] if fila else None


def ordenar_por_tipo(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY tipo, nombre").fetchall()]
