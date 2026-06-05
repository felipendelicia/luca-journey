# Líder Maylene — Ranking del Dojo (solución de referencia).
# El preamble (conexion + tabla pokemon) está en meta.json y se antepone al corregir.

def de_tipo(conexion, tipo):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon WHERE tipo = ?", (tipo,))]

def fuertes(conexion, minimo):
    return [f[0] for f in conexion.execute(
        "SELECT nombre FROM pokemon WHERE nivel >= ? ORDER BY nivel DESC", (minimo,))]

def ordenados_por_nivel(conexion):
    return [f[0] for f in conexion.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC")]

def top_tres(conexion):
    return [f[0] for f in conexion.execute(
        "SELECT nombre FROM pokemon ORDER BY nivel DESC LIMIT 3")]
