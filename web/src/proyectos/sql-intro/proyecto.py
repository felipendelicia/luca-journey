# Líder Roark — Registro de la Mina (solución de referencia).
# El preamble (conexion + tabla pokemon) está en meta.json y se antepone al corregir.

def todos_los_nombres(conexion):
    return [fila[0] for fila in conexion.execute("SELECT nombre FROM pokemon")]

def cuantos_hay(conexion):
    return conexion.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]

def nombres_y_niveles(conexion):
    return [(fila[0], fila[1]) for fila in conexion.execute("SELECT nombre, nivel FROM pokemon")]

def el_primero(conexion):
    return conexion.execute("SELECT nombre FROM pokemon LIMIT 1").fetchone()[0]
