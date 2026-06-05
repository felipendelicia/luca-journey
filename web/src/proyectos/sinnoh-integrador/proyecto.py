# Integrador de Sinnoh — La Pokédex Completa (solución de referencia).
# El preamble (import sqlite3) está en meta.json y se antepone al corregir.

def crear_base():
    conexion = sqlite3.connect(":memory:")
    conexion.execute("CREATE TABLE tipos (tipo TEXT, debilidad TEXT)")
    conexion.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT, nivel INTEGER)")
    return conexion

def cargar_datos(conexion):
    conexion.executemany("INSERT INTO tipos VALUES (?, ?)", [
        ("Agua",     "Planta"),
        ("Fuego",    "Agua"),
        ("Planta",   "Fuego"),
        ("Dragon",   "Hielo"),
        ("Psiquico", "Siniestro"),
    ])
    conexion.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", [
        ("Piplup",    "Agua",     15),
        ("Empoleon",  "Agua",     58),
        ("Chimchar",  "Fuego",    14),
        ("Infernape", "Fuego",    62),
        ("Turtwig",   "Planta",   13),
        ("Torterra",  "Planta",   55),
        ("Garchomp",  "Dragon",   66),
        ("Alakazam",  "Psiquico", 54),
    ])

def promedio_por_tipo(conexion):
    filas = conexion.execute("SELECT tipo, AVG(nivel) FROM pokemon GROUP BY tipo")
    return {tipo: prom for tipo, prom in filas}

def el_mas_fuerte_por_tipo(conexion):
    filas = conexion.execute(
        "SELECT tipo, nombre FROM pokemon WHERE nivel = "
        "(SELECT MAX(nivel) FROM pokemon p2 WHERE p2.tipo = pokemon.tipo) "
        "GROUP BY tipo"
    )
    return {tipo: nombre for tipo, nombre in filas}

def con_debilidad(conexion):
    sql = "SELECT p.nombre, t.debilidad FROM pokemon p JOIN tipos t ON p.tipo = t.tipo"
    return [(f[0], f[1]) for f in conexion.execute(sql)]

def mas_debiles_a(conexion, elemento):
    sql = ("SELECT p.nombre FROM pokemon p JOIN tipos t ON p.tipo = t.tipo "
           "WHERE t.debilidad = ? ORDER BY p.nivel DESC")
    return [f[0] for f in conexion.execute(sql, (elemento,))]

def buscar(conexion, nombre):
    return conexion.execute(
        "SELECT nombre, tipo, nivel FROM pokemon WHERE nombre = ?", (nombre,)
    ).fetchone()

def evolucionar(conexion, nombre, nuevo_nombre, nuevo_nivel):
    conexion.execute(
        "UPDATE pokemon SET nombre = ?, nivel = ? WHERE nombre = ?",
        (nuevo_nombre, nuevo_nivel, nombre)
    )
    conexion.commit()
