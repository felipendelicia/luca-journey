"""✏️ Ejercicios — SQL: crear e insertar

Creamos tablas (CREATE TABLE) y metemos datos (INSERT). La conexión te llega vacía.
✅ Corregir al terminar.
"""
import sqlite3


# Crear una tabla
# Creá una tabla 'entrenadores' con columnas: nombre (TEXT) y medallas (INTEGER).
# Pista: conexion.execute("CREATE TABLE entrenadores (nombre TEXT, medallas INTEGER)").
def crear_tabla(conexion):
    """Creá la tabla 'entrenadores'."""
    # TU CÓDIGO ACÁ
    pass


# Insertar uno
# Insertá UN entrenador en la tabla (ya creada). Usá parámetros (?) por seguridad.
# Pista: conexion.execute("INSERT INTO entrenadores VALUES (?, ?)", (nombre, medallas)).
def insertar(conexion, nombre, medallas):
    """Insertá un entrenador (nombre, medallas)."""
    # TU CÓDIGO ACÁ
    pass


# Insertar varios
# Insertá VARIOS entrenadores de una. 'filas' es una lista de tuplas (nombre, medallas).
# Pista: conexion.executemany("INSERT INTO entrenadores VALUES (?, ?)", filas).
def insertar_varios(conexion, filas):
    """Insertá todas las filas de una."""
    # TU CÓDIGO ACÁ
    pass


# Crear + insertar
# Creá la tabla 'pokemon' (nombre TEXT, nivel INTEGER) e insertá a ('Pikachu', 25).
def crear_pokedex(conexion):
    """Creá la tabla y meté ('Pikachu', 25)."""
    # TU CÓDIGO ACÁ
    pass


# Contar
# Devolvé cuántos entrenadores hay. Pista: SELECT COUNT(*) FROM entrenadores.
def contar(conexion):
    """Devolvé cuántos entrenadores hay."""
    # TU CÓDIGO ACÁ
    pass


# Todos los nombres
# Devolvé los NOMBRES de los entrenadores.
def todos_los_nombres(conexion):
    """Devolvé los nombres."""
    # TU CÓDIGO ACÁ
    pass


# Medallas de uno
# Devolvé las medallas del entrenador `nombre`, o None si no está.
def medallas_de(conexion, nombre):
    """Devolvé las medallas de ese entrenador, o None."""
    # TU CÓDIGO ACÁ
    pass


# Total de medallas
# Devolvé la suma de las medallas de todos. Pista: SUM(medallas).
def total_medallas(conexion):
    """Devolvé la suma de medallas."""
    # TU CÓDIGO ACÁ
    pass


# Promedio de medallas
# Devolvé el promedio de medallas. Pista: AVG(medallas).
def promedio_medallas(conexion):
    """Devolvé el promedio de medallas."""
    # TU CÓDIGO ACÁ
    pass


# El mejor
# Devolvé el NOMBRE del entrenador con más medallas. Pista: ORDER BY medallas DESC LIMIT 1.
def el_mejor(conexion):
    """Devolvé el de más medallas."""
    # TU CÓDIGO ACÁ
    pass


# Con más de n medallas
# Devolvé los NOMBRES con más de `n` medallas.
def con_mas_de(conexion, n):
    """Devolvé los nombres con medallas > n."""
    # TU CÓDIGO ACÁ
    pass


# Ordenados por medallas
# Devolvé los NOMBRES ordenados de más a menos medallas.
def ordenados_por_medallas(conexion):
    """Devolvé los nombres ordenados por medallas (desc)."""
    # TU CÓDIGO ACÁ
    pass


# ¿Existe?
# Devolvé True si hay un entrenador con ese `nombre`.
def existe(conexion, nombre):
    """Devolvé True si está ese entrenador."""
    # TU CÓDIGO ACÁ
    pass


# Insertar si no existe
# Insertá (nombre, medallas) SOLO si todavía no hay un entrenador con ese nombre.
def insertar_si_no_existe(conexion, nombre, medallas):
    """Insertá solo si no existe ese nombre."""
    # TU CÓDIGO ACÁ
    pass


# Máximo de medallas
# Devolvé la mayor cantidad de medallas. Pista: MAX(medallas).
def maximo_medallas(conexion):
    """Devolvé el máximo de medallas."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad con cierto número
# Devolvé cuántos entrenadores tienen exactamente `medallas` medallas.
def cantidad_con(conexion, medallas):
    """Devolvé cuántos tienen esa cantidad de medallas."""
    # TU CÓDIGO ACÁ
    pass


# Nombre y medallas
# Devolvé una lista de tuplas (nombre, medallas).
def nombres_y_medallas(conexion):
    """Devolvé pares (nombre, medallas)."""
    # TU CÓDIGO ACÁ
    pass


# Vaciar
# Borrá todos los entrenadores. Pista: DELETE FROM entrenadores.
def vaciar(conexion):
    """Borrá todos los entrenadores."""
    # TU CÓDIGO ACÁ
    pass


# Actualizar medallas
# Poné las medallas del entrenador `nombre` en `medallas`.
def actualizar_medallas(conexion, nombre, medallas):
    """Actualizá las medallas de ese entrenador."""
    # TU CÓDIGO ACÁ
    pass


# Campeones
# Devolvé los NOMBRES con `minimo` medallas o más.
def campeones(conexion, minimo):
    """Devolvé los nombres con medallas >= minimo."""
    # TU CÓDIGO ACÁ
    pass
