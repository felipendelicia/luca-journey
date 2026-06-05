# Líder Byron — Debilidades del Castillo (solución de referencia).
# El preamble (conexion + tablas pokemon y tipos) está en meta.json y se antepone al corregir.

def con_debilidad(conexion):
    sql = "SELECT p.nombre, t.debilidad FROM pokemon p JOIN tipos t ON p.tipo = t.tipo"
    return [(f[0], f[1]) for f in conexion.execute(sql)]

def debilidad_de(conexion, nombre):
    sql = "SELECT t.debilidad FROM pokemon p JOIN tipos t ON p.tipo = t.tipo WHERE p.nombre = ?"
    return conexion.execute(sql, (nombre,)).fetchone()[0]

def nombres_y_tipos(conexion):
    return [(f[0], f[1]) for f in conexion.execute("SELECT nombre, tipo FROM pokemon")]

def debiles_a(conexion, elemento):
    sql = ("SELECT p.nombre FROM pokemon p JOIN tipos t ON p.tipo = t.tipo "
           "WHERE t.debilidad = ? ORDER BY p.nombre")
    return [f[0] for f in conexion.execute(sql, (elemento,))]
