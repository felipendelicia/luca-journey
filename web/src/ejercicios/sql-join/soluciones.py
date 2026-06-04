"""✅ Soluciones — SQL: relaciones y JOIN"""
import sqlite3


def con_debilidad(conexion):
    sql = "SELECT p.nombre, t.debilidad FROM pokemon p JOIN tipos t ON p.tipo = t.tipo"
    return [(f[0], f[1]) for f in conexion.execute(sql)]


def debilidad_de(conexion, nombre):
    sql = "SELECT t.debilidad FROM pokemon p JOIN tipos t ON p.tipo = t.tipo WHERE p.nombre = ?"
    return conexion.execute(sql, (nombre,)).fetchone()[0]


def debiles_a(conexion, elemento):
    sql = "SELECT p.nombre FROM pokemon p JOIN tipos t ON p.tipo = t.tipo WHERE t.debilidad = ?"
    return [f[0] for f in conexion.execute(sql, (elemento,))]
