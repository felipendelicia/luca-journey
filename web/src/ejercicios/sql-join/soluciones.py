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


def nombres_y_debilidad(conexion):
    return [(f[0], f[1]) for f in conexion.execute("SELECT p.nombre, t.debilidad FROM pokemon p JOIN tipos t ON p.tipo = t.tipo").fetchall()]


def cuantos_debiles_a(conexion, elemento):
    return conexion.execute("SELECT COUNT(*) FROM pokemon p JOIN tipos t ON p.tipo = t.tipo WHERE t.debilidad = ?", (elemento,)).fetchone()[0]


def tipos_con_debilidad(conexion):
    return [(f[0], f[1]) for f in conexion.execute("SELECT tipo, debilidad FROM tipos").fetchall()]


def debilidad_del_tipo(conexion, tipo):
    fila = conexion.execute("SELECT debilidad FROM tipos WHERE tipo = ?", (tipo,)).fetchone()
    return fila[0] if fila else None


def sin_debilidad_conocida(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE tipo NOT IN (SELECT tipo FROM tipos)").fetchall()]


def con_debilidad_conocida(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE tipo IN (SELECT tipo FROM tipos)").fetchall()]


def contar_join(conexion):
    return conexion.execute("SELECT COUNT(*) FROM pokemon p JOIN tipos t ON p.tipo = t.tipo").fetchone()[0]


def mapa_debilidades(conexion):
    return {f[0]: f[1] for f in conexion.execute("SELECT tipo, debilidad FROM tipos").fetchall()}


def tipos_de_pokemon(conexion):
    return [f[0] for f in conexion.execute("SELECT DISTINCT tipo FROM pokemon ORDER BY tipo").fetchall()]


def debilidades_distintas(conexion):
    return [f[0] for f in conexion.execute("SELECT DISTINCT debilidad FROM tipos ORDER BY debilidad").fetchall()]


def nombre_tipo_debilidad(conexion):
    return [(f[0], f[1], f[2]) for f in conexion.execute("SELECT p.nombre, p.tipo, t.debilidad FROM pokemon p JOIN tipos t ON p.tipo = t.tipo").fetchall()]


def hay_debilidad_para(conexion, tipo):
    return conexion.execute("SELECT 1 FROM tipos WHERE tipo = ?", (tipo,)).fetchone() is not None


def primer_debil_a(conexion, elemento):
    fila = conexion.execute("SELECT p.nombre FROM pokemon p JOIN tipos t ON p.tipo = t.tipo WHERE t.debilidad = ? LIMIT 1", (elemento,)).fetchone()
    return fila[0] if fila else None


def tipos_que_pierden_contra(conexion, elemento):
    return [f[0] for f in conexion.execute("SELECT tipo FROM tipos WHERE debilidad = ?", (elemento,)).fetchall()]


def cuantos_de_tipo(conexion, tipo):
    return conexion.execute("SELECT COUNT(*) FROM pokemon WHERE tipo = ?", (tipo,)).fetchone()[0]


def nombres_debiles_ordenados(conexion):
    return [f[0] for f in conexion.execute("SELECT p.nombre FROM pokemon p JOIN tipos t ON p.tipo = t.tipo ORDER BY p.nombre").fetchall()]


def todos_los_nombres(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon").fetchall()]
