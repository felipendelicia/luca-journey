"""✅ Soluciones — SQL: crear e insertar"""
import sqlite3


def crear_tabla(conexion):
    conexion.execute("CREATE TABLE entrenadores (nombre TEXT, medallas INTEGER)")


def insertar(conexion, nombre, medallas):
    conexion.execute("INSERT INTO entrenadores VALUES (?, ?)", (nombre, medallas))


def insertar_varios(conexion, filas):
    conexion.executemany("INSERT INTO entrenadores VALUES (?, ?)", filas)


def crear_pokedex(conexion):
    conexion.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
    conexion.execute("INSERT INTO pokemon VALUES (?, ?)", ("Pikachu", 25))


def contar(conexion):
    return conexion.execute("SELECT COUNT(*) FROM entrenadores").fetchone()[0]


def todos_los_nombres(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM entrenadores").fetchall()]


def medallas_de(conexion, nombre):
    fila = conexion.execute("SELECT medallas FROM entrenadores WHERE nombre = ?", (nombre,)).fetchone()
    return fila[0] if fila else None


def total_medallas(conexion):
    return conexion.execute("SELECT SUM(medallas) FROM entrenadores").fetchone()[0]


def promedio_medallas(conexion):
    return conexion.execute("SELECT AVG(medallas) FROM entrenadores").fetchone()[0]


def el_mejor(conexion):
    return conexion.execute("SELECT nombre FROM entrenadores ORDER BY medallas DESC LIMIT 1").fetchone()[0]


def con_mas_de(conexion, n):
    return [f[0] for f in conexion.execute("SELECT nombre FROM entrenadores WHERE medallas > ?", (n,)).fetchall()]


def ordenados_por_medallas(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM entrenadores ORDER BY medallas DESC").fetchall()]


def existe(conexion, nombre):
    return conexion.execute("SELECT 1 FROM entrenadores WHERE nombre = ?", (nombre,)).fetchone() is not None


def insertar_si_no_existe(conexion, nombre, medallas):
    if not existe(conexion, nombre):
        conexion.execute("INSERT INTO entrenadores VALUES (?, ?)", (nombre, medallas))
        conexion.commit()


def maximo_medallas(conexion):
    return conexion.execute("SELECT MAX(medallas) FROM entrenadores").fetchone()[0]


def cantidad_con(conexion, medallas):
    return conexion.execute("SELECT COUNT(*) FROM entrenadores WHERE medallas = ?", (medallas,)).fetchone()[0]


def nombres_y_medallas(conexion):
    return [(f[0], f[1]) for f in conexion.execute("SELECT nombre, medallas FROM entrenadores").fetchall()]


def vaciar(conexion):
    conexion.execute("DELETE FROM entrenadores")
    conexion.commit()


def actualizar_medallas(conexion, nombre, medallas):
    conexion.execute("UPDATE entrenadores SET medallas = ? WHERE nombre = ?", (medallas, nombre))
    conexion.commit()


def campeones(conexion, minimo):
    return [f[0] for f in conexion.execute("SELECT nombre FROM entrenadores WHERE medallas >= ?", (minimo,)).fetchall()]
