"""✏️ Ejercicios — SQLite desde Python

Hasta ahora escribiste SQL. Acá lo manejás DESDE Python con el módulo sqlite3:
conectarte, ejecutar, traer resultados (fetchone/fetchall) y guardar (commit).
✅ Corregir al terminar.
"""
import sqlite3


# Crear la conexión
# Creá una base en memoria con una tabla 'pokemon' (nombre TEXT, nivel INTEGER) y
# devolvé la conexión. Pista: sqlite3.connect(":memory:") y un CREATE TABLE.
def crear_conexion():
    """Devolvé una conexión con la tabla 'pokemon' ya creada."""
    # TU CÓDIGO ACÁ
    pass


# Guardar con commit
# Insertá un Pokémon en la tabla y confirmá con commit(). Pista: INSERT con (?) + conexion.commit().
def guardar(conexion, nombre, nivel):
    """Insertá (nombre, nivel) y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# Contar con cursor
# Devolvé cuántos Pokémon hay, usando un cursor y fetchone().
# Pista: cur = conexion.cursor(); cur.execute("SELECT COUNT(*) ..."); return cur.fetchone()[0].
def cantidad(conexion):
    """Devolvé la cantidad de Pokémon (int)."""
    # TU CÓDIGO ACÁ
    pass


# Buscar uno (o None)
# Buscá un Pokémon por nombre. Devolvé su fila (tupla) o None si no existe.
# Pista: SELECT * ... WHERE nombre = ?  →  .fetchone()  (devuelve None si no hay).
# Ejemplo:  buscar(con, "Eevee")  →  ("Eevee", 15)   ·   buscar(con, "Mew")  →  None
def buscar(conexion, nombre):
    """Devolvé la fila del Pokémon, o None."""
    # TU CÓDIGO ACÁ
    pass


# Todos los nombres
# Devolvé los NOMBRES de todos los Pokémon, como lista.
def todos(conexion):
    """Devolvé todos los nombres."""
    # TU CÓDIGO ACÁ
    pass


# Niveles
# Devolvé la lista de niveles.
def niveles(conexion):
    """Devolvé la lista de niveles."""
    # TU CÓDIGO ACÁ
    pass


# Actualizar nivel
# Poné el nivel del Pokémon `nombre` en `nivel` y hacé commit.
def actualizar(conexion, nombre, nivel):
    """Actualizá el nivel y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# Borrar
# Borrá el Pokémon `nombre` y hacé commit.
def borrar(conexion, nombre):
    """Borrá ese Pokémon y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# ¿Existe?
# Devolvé True si hay un Pokémon con ese `nombre`.
def existe(conexion, nombre):
    """Devolvé True si está ese Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Nivel de uno
# Devolvé el nivel del Pokémon `nombre`, o None si no está.
def nivel_de(conexion, nombre):
    """Devolvé el nivel de ese Pokémon, o None."""
    # TU CÓDIGO ACÁ
    pass


# Promedio
# Devolvé el nivel promedio. Pista: AVG(nivel).
def promedio(conexion):
    """Devolvé el promedio de nivel."""
    # TU CÓDIGO ACÁ
    pass


# Máximo
# Devolvé el nivel más alto. Pista: MAX(nivel).
def maximo(conexion):
    """Devolvé el nivel máximo."""
    # TU CÓDIGO ACÁ
    pass


# Guardar varios
# Insertá varias filas de una con `executemany` y hacé commit. `filas` es una lista de
# tuplas (nombre, nivel).
def guardar_varios(conexion, filas):
    """Insertá varias filas y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# El más fuerte
# Devolvé el NOMBRE del Pokémon de mayor nivel.
def mas_fuerte(conexion):
    """Devolvé el nombre del de mayor nivel."""
    # TU CÓDIGO ACÁ
    pass


# Ordenados por nivel
# Devolvé los NOMBRES ordenados de mayor a menor nivel.
def ordenados(conexion):
    """Devolvé los nombres ordenados por nivel (desc)."""
    # TU CÓDIGO ACÁ
    pass


# Contar por encima de un nivel
# Devolvé cuántos Pokémon tienen nivel mayor que `n`.
def contar_arriba(conexion, n):
    """Devolvé cuántos tienen nivel > n."""
    # TU CÓDIGO ACÁ
    pass


# Vaciar
# Borrá todos los Pokémon y hacé commit.
def vaciar(conexion):
    """Borrá todos y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# A diccionario
# Devolvé un dict nombre → nivel con todos los Pokémon.
def a_diccionario(conexion):
    """Devolvé un dict nombre → nivel."""
    # TU CÓDIGO ACÁ
    pass


# Subir nivel
# Sumá `cuanto` al nivel del Pokémon `nombre` y hacé commit.
def subir_nivel(conexion, nombre, cuanto):
    """Subí el nivel de un Pokémon y hacé commit."""
    # TU CÓDIGO ACÁ
    pass


# Total de niveles
# Devolvé la suma de todos los niveles. Pista: SUM(nivel).
def total_niveles(conexion):
    """Devolvé la suma de los niveles."""
    # TU CÓDIGO ACÁ
    pass
