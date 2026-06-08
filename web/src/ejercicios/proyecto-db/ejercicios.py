"""✏️ Ejercicios — Proyecto: Pokédex en SQLite

Tu Pokédex guardada en una base de datos. Junta todo Sinnoh: crear, insertar, consultar
y agrupar — desde Python. Tabla 'pokemon' (nombre, tipo, nivel). ✅ Corregir al terminar.
"""
import sqlite3


# Crear la Pokédex
# Creá la base con la tabla 'pokemon' (nombre TEXT, tipo TEXT, nivel INTEGER) y devolvé
# la conexión.
def crear_pokedex():
    """Devolvé una conexión con la tabla 'pokemon' lista."""
    # TU CÓDIGO ACÁ
    pass


# Agregar un Pokémon
# Insertá un Pokémon y confirmá (commit). Pista: INSERT con (?) + commit.
def agregar(conexion, nombre, tipo, nivel):
    """Insertá (nombre, tipo, nivel) y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# Listar (ordenado)
# Devolvé los nombres de todos, ordenados alfabéticamente. Pista: SELECT nombre ... ORDER BY nombre.
def listar(conexion):
    """Devolvé la lista de nombres ordenada."""
    # TU CÓDIGO ACÁ
    pass


# Por tipo
# Devolvé los nombres de un tipo dado. Pista: WHERE tipo = ?.
# Ejemplo:  por_tipo(con, "Fuego")  →  ["Charizard", "Vulpix"]
def por_tipo(conexion, tipo):
    """Devolvé los nombres de ese 'tipo'."""
    # TU CÓDIGO ACÁ
    pass


# El más fuerte
# Devolvé el NOMBRE del Pokémon de mayor nivel. Pista: ORDER BY nivel DESC LIMIT 1 → fetchone()[0].
def el_mas_fuerte(conexion):
    """Devolvé el nombre del de mayor nivel."""
    # TU CÓDIGO ACÁ
    pass


# Cuántos por tipo
# Devolvé un dict {tipo: cantidad}. Pista: SELECT tipo, COUNT(*) ... GROUP BY tipo.
# Ejemplo:  cuantos_por_tipo(con)  →  {"Fuego": 2, "Electrico": 1}
def cuantos_por_tipo(conexion):
    """Devolvé un dict {tipo: cantidad}."""
    # TU CÓDIGO ACÁ
    pass


# Contar
# Devolvé cuántos Pokémon hay en la Pokédex.
def contar(conexion):
    """Devolvé cuántos Pokémon hay."""
    # TU CÓDIGO ACÁ
    pass


# Nombres
# Devolvé los NOMBRES de todos los Pokémon, como lista.
def nombres(conexion):
    """Devolvé los nombres."""
    # TU CÓDIGO ACÁ
    pass


# Nivel promedio
# Devolvé el nivel promedio. Pista: AVG(nivel).
def nivel_promedio(conexion):
    """Devolvé el nivel promedio."""
    # TU CÓDIGO ACÁ
    pass


# Tipos
# Devolvé los tipos DISTINTOS, ordenados.
def tipos(conexion):
    """Devolvé los tipos distintos, ordenados."""
    # TU CÓDIGO ACÁ
    pass


# Borrar
# Borrá el Pokémon `nombre` y hacé commit.
def borrar(conexion, nombre):
    """Borrá ese Pokémon y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# Subir nivel
# Sumá `cuanto` al nivel del Pokémon `nombre` y hacé commit.
def subir_nivel(conexion, nombre, cuanto):
    """Subí el nivel de un Pokémon y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# Buscar
# Devolvé la fila completa (tupla) del Pokémon `nombre`, o None si no está.
def buscar(conexion, nombre):
    """Devolvé la fila del Pokémon, o None."""
    # TU CÓDIGO ACÁ
    pass


# ¿Existe?
# Devolvé True si hay un Pokémon con ese `nombre`.
def existe(conexion, nombre):
    """Devolvé True si está ese Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# El más débil
# Devolvé el NOMBRE del Pokémon de menor nivel.
def mas_debil(conexion):
    """Devolvé el nombre del de menor nivel."""
    # TU CÓDIGO ACÁ
    pass


# De nivel mínimo
# Devolvé los NOMBRES de los Pokémon con nivel mayor o igual a `minimo`.
def de_nivel_minimo(conexion, minimo):
    """Devolvé los nombres con nivel >= minimo."""
    # TU CÓDIGO ACÁ
    pass


# Nivel total
# Devolvé la suma de todos los niveles.
def nivel_total(conexion):
    """Devolvé la suma de los niveles."""
    # TU CÓDIGO ACÁ
    pass


# Promedio por tipo
# Devolvé un dict tipo → nivel promedio. Pista: SELECT tipo, AVG(nivel) ... GROUP BY tipo.
def promedio_por_tipo(conexion):
    """Devolvé un dict tipo → nivel promedio."""
    # TU CÓDIGO ACÁ
    pass


# Renombrar
# Cambiá el nombre del Pokémon `viejo` a `nuevo` y hacé commit.
def renombrar(conexion, viejo, nuevo):
    """Renombrá un Pokémon y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# Ordenados por nivel
# Devolvé los NOMBRES ordenados de mayor a menor nivel.
def ordenados_por_nivel(conexion):
    """Devolvé los nombres ordenados por nivel (desc)."""
    # TU CÓDIGO ACÁ
    pass
