# Líder Fantina — Estadísticas del Concurso (solución de referencia).
# El preamble (conexion + tabla pokemon) está en meta.json y se antepone al corregir.

def nivel_promedio(conexion):
    return conexion.execute("SELECT AVG(nivel) FROM pokemon").fetchone()[0]

def nivel_maximo(conexion):
    return conexion.execute("SELECT MAX(nivel) FROM pokemon").fetchone()[0]

def cuantos_por_tipo(conexion):
    filas = conexion.execute("SELECT tipo, COUNT(*) FROM pokemon GROUP BY tipo")
    return {tipo: cant for tipo, cant in filas}

def promedio_por_tipo(conexion):
    filas = conexion.execute("SELECT tipo, AVG(nivel) FROM pokemon GROUP BY tipo")
    return {tipo: prom for tipo, prom in filas}
