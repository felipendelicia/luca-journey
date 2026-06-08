"""✅ Soluciones — Proyecto: Pokédex en SQLite"""
import sqlite3


def crear_pokedex():
    conexion = sqlite3.connect(":memory:")
    conexion.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT, nivel INTEGER)")
    return conexion


def agregar(conexion, nombre, tipo, nivel):
    conexion.execute("INSERT INTO pokemon VALUES (?, ?, ?)", (nombre, tipo, nivel))
    conexion.commit()


def listar(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY nombre")]


def por_tipo(conexion, tipo):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE tipo = ?", (tipo,))]


def el_mas_fuerte(conexion):
    return conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC LIMIT 1").fetchone()[0]


def cuantos_por_tipo(conexion):
    filas = conexion.execute("SELECT tipo, COUNT(*) FROM pokemon GROUP BY tipo")
    return {tipo: cant for tipo, cant in filas}


def contar(conexion):
    return conexion.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]


def nombres(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon").fetchall()]


def nivel_promedio(conexion):
    return conexion.execute("SELECT AVG(nivel) FROM pokemon").fetchone()[0]


def tipos(conexion):
    return [f[0] for f in conexion.execute("SELECT DISTINCT tipo FROM pokemon ORDER BY tipo").fetchall()]


def borrar(conexion, nombre):
    conexion.execute("DELETE FROM pokemon WHERE nombre = ?", (nombre,))
    conexion.commit()


def subir_nivel(conexion, nombre, cuanto):
    conexion.execute("UPDATE pokemon SET nivel = nivel + ? WHERE nombre = ?", (cuanto, nombre))
    conexion.commit()


def buscar(conexion, nombre):
    return conexion.execute("SELECT * FROM pokemon WHERE nombre = ?", (nombre,)).fetchone()


def existe(conexion, nombre):
    return conexion.execute("SELECT 1 FROM pokemon WHERE nombre = ?", (nombre,)).fetchone() is not None


def mas_debil(conexion):
    return conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel ASC LIMIT 1").fetchone()[0]


def de_nivel_minimo(conexion, minimo):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE nivel >= ?", (minimo,)).fetchall()]


def nivel_total(conexion):
    return conexion.execute("SELECT SUM(nivel) FROM pokemon").fetchone()[0]


def promedio_por_tipo(conexion):
    return {f[0]: f[1] for f in conexion.execute("SELECT tipo, AVG(nivel) FROM pokemon GROUP BY tipo").fetchall()}


def renombrar(conexion, viejo, nuevo):
    conexion.execute("UPDATE pokemon SET nombre = ? WHERE nombre = ?", (nuevo, viejo))
    conexion.commit()


def ordenados_por_nivel(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC").fetchall()]
