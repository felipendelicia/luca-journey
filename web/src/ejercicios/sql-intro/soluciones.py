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
