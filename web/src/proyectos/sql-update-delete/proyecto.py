# Líder Crasher Wake — Gestión del Lago (solución de referencia).
# El preamble (conexion + tabla pokemon) está en meta.json y se antepone al corregir.

def cambiar_nivel(conexion, nombre, nuevo_nivel):
    conexion.execute("UPDATE pokemon SET nivel = ? WHERE nombre = ?", (nuevo_nivel, nombre))

def subir_todos(conexion, cuanto):
    conexion.execute("UPDATE pokemon SET nivel = nivel + ?", (cuanto,))

def borrar(conexion, nombre):
    conexion.execute("DELETE FROM pokemon WHERE nombre = ?", (nombre,))

def borrar_debiles(conexion, umbral):
    conexion.execute("DELETE FROM pokemon WHERE nivel < ?", (umbral,))
