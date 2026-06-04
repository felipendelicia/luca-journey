"""
✏️ Ejercicios — SQL: actualizar y borrar

UPDATE cambia datos existentes; DELETE los elimina. Siempre con WHERE
(¡sin WHERE afecta TODA la tabla!). Tabla 'pokemon' (nombre, nivel, tipo).
"""
import sqlite3


# 1) Cambiá el nivel de un Pokémon. UPDATE ... SET nivel = ? WHERE nombre = ?.
def cambiar_nivel(conexion, nombre, nuevo_nivel):
    """Actualizá el nivel del Pokémon 'nombre'."""
    # TU CÓDIGO ACÁ
    pass


# 2) Subí el nivel de TODOS en 'cuanto'. UPDATE ... SET nivel = nivel + ?.
def subir_todos(conexion, cuanto):
    """Sumale 'cuanto' al nivel de cada Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# 3) Borrá un Pokémon por nombre. DELETE FROM ... WHERE nombre = ?.
def borrar(conexion, nombre):
    """Eliminá el Pokémon 'nombre'."""
    # TU CÓDIGO ACÁ
    pass


# 4) Borrá los Pokémon con nivel menor a 'umbral'. DELETE ... WHERE nivel < ?.
def borrar_debiles(conexion, umbral):
    """Eliminá los que tengan nivel < umbral."""
    # TU CÓDIGO ACÁ
    pass
