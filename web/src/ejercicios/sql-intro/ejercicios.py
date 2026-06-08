"""✏️ Ejercicios — SQL: leer datos

Una base de datos guarda info en TABLAS (filas y columnas), como un Excel. Cada función
recibe una conexión a una base con la tabla 'pokemon' (columnas: nombre, nivel, tipo).
Vos escribís el SQL. ✅ Corregir al terminar.
"""
import sqlite3


# Leer los nombres
# Devolvé los NOMBRES de todos los Pokémon. Pista: SELECT nombre FROM pokemon.
# Ejemplo:  devuelve  ["Pikachu", "Charizard", "Bulbasaur"]
def todos(conexion):
    """Devolvé una lista con los nombres."""
    # TU CÓDIGO ACÁ
    pass


# ¿Cuántos hay?
# Devolvé cuántos Pokémon hay. Pista: SELECT COUNT(*) FROM pokemon  →  .fetchone()[0].
# Ejemplo:  con 3 Pokémon en la tabla  →  3
def cuantos(conexion):
    """Devolvé un número entero."""
    # TU CÓDIGO ACÁ
    pass


# La columna nivel
# Devolvé la lista de NIVELES (la columna 'nivel').
# Ejemplo:  devuelve  [25, 90, 12]
def niveles(conexion):
    """Devolvé una lista de enteros."""
    # TU CÓDIGO ACÁ
    pass


# Nombre y nivel
# Devolvé pares (nombre, nivel) de cada Pokémon. Pista: SELECT nombre, nivel ...
# Ejemplo:  [("Pikachu", 25), ("Charizard", 90)]
def nombres_y_niveles(conexion):
    """Devolvé una lista de tuplas (nombre, nivel)."""
    # TU CÓDIGO ACÁ
    pass


# El primero
# Devolvé el nombre del PRIMER Pokémon de la tabla. Pista: LIMIT 1  →  .fetchone()[0].
# Ejemplo:  "Pikachu"
def primero(conexion):
    """Devolvé el nombre del primero (str)."""
    # TU CÓDIGO ACÁ
    pass


# Ordenados por nivel
# Devolvé los NOMBRES ordenados de mayor a menor nivel. Pista: ORDER BY nivel DESC.
def ordenados_por_nivel(conexion):
    """Devolvé los nombres ordenados por nivel (desc)."""
    # TU CÓDIGO ACÁ
    pass


# Más de cierto nivel
# Devolvé los NOMBRES de los Pokémon con nivel mayor que `n`. Pista: WHERE nivel > ?.
def mas_de(conexion, n):
    """Devolvé los nombres con nivel > n."""
    # TU CÓDIGO ACÁ
    pass


# De un tipo
# Devolvé los NOMBRES de los Pokémon de tipo `tipo`. Pista: WHERE tipo = ?.
def de_tipo(conexion, tipo):
    """Devolvé los nombres de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Promedio de nivel
# Devolvé el nivel PROMEDIO. Pista: SELECT AVG(nivel) ...  →  .fetchone()[0].
def promedio_nivel(conexion):
    """Devolvé el promedio de nivel."""
    # TU CÓDIGO ACÁ
    pass


# Máximo nivel
# Devolvé el nivel más alto. Pista: SELECT MAX(nivel) ...
def maximo_nivel(conexion):
    """Devolvé el nivel máximo."""
    # TU CÓDIGO ACÁ
    pass


# Mínimo nivel
# Devolvé el nivel más bajo. Pista: SELECT MIN(nivel) ...
def minimo_nivel(conexion):
    """Devolvé el nivel mínimo."""
    # TU CÓDIGO ACÁ
    pass


# Nivel total
# Devolvé la suma de todos los niveles. Pista: SELECT SUM(nivel) ...
def nivel_total(conexion):
    """Devolvé la suma de los niveles."""
    # TU CÓDIGO ACÁ
    pass


# Contar de un tipo
# Devolvé cuántos Pokémon hay de tipo `tipo`. Pista: SELECT COUNT(*) ... WHERE tipo = ?.
def contar_de_tipo(conexion, tipo):
    """Devolvé cuántos son de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# El más fuerte
# Devolvé el NOMBRE del Pokémon de mayor nivel. Pista: ORDER BY nivel DESC LIMIT 1.
def el_mas_fuerte(conexion):
    """Devolvé el nombre del de mayor nivel."""
    # TU CÓDIGO ACÁ
    pass


# Tipos distintos
# Devolvé los tipos distintos ORDENADOS. Pista: SELECT DISTINCT tipo ... ORDER BY tipo.
def tipos_distintos(conexion):
    """Devolvé los tipos distintos, ordenados."""
    # TU CÓDIGO ACÁ
    pass


# ¿Existe?
# Devolvé True si hay un Pokémon con ese `nombre`.
def existe(conexion, nombre):
    """Devolvé True si está ese nombre."""
    # TU CÓDIGO ACÁ
    pass


# Nivel de uno
# Devolvé el nivel del Pokémon con ese `nombre`, o None si no está.
def nivel_de(conexion, nombre):
    """Devolvé el nivel de ese Pokémon, o None."""
    # TU CÓDIGO ACÁ
    pass


# Los primeros n
# Devolvé los NOMBRES de los primeros `n` Pokémon. Pista: LIMIT ?.
def primeros(conexion, n):
    """Devolvé los primeros n nombres."""
    # TU CÓDIGO ACÁ
    pass


# Que empiezan con
# Devolvé los NOMBRES que empiezan con `letra`. Pista: WHERE nombre LIKE ? con `letra + "%"`.
def nombres_que_empiezan(conexion, letra):
    """Devolvé los nombres que empiezan con letra."""
    # TU CÓDIGO ACÁ
    pass


# Ordenados alfabéticamente
# Devolvé los NOMBRES ordenados de la A a la Z. Pista: ORDER BY nombre.
def ordenados_alfabeticamente(conexion):
    """Devolvé los nombres ordenados alfabéticamente."""
    # TU CÓDIGO ACÁ
    pass
