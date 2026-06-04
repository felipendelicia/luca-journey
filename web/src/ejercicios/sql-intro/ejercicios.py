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
