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
