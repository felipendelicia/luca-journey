"""✏️ Ejercicios — SQL: actualizar y borrar

UPDATE cambia datos existentes; DELETE los elimina. SIEMPRE con WHERE (¡sin WHERE
afecta TODA la tabla!). Tabla 'pokemon' (nombre, nivel, tipo). ✅ Corregir al terminar.
"""
import sqlite3


# Cambiar el nivel
# Cambiá el nivel de un Pokémon. Pista: UPDATE pokemon SET nivel = ? WHERE nombre = ?.
# Ejemplo:  cambiar_nivel(con, "Pikachu", 50)  deja a Pikachu en nivel 50.
def cambiar_nivel(conexion, nombre, nuevo_nivel):
    """Actualizá el nivel del Pokémon 'nombre'."""
    # TU CÓDIGO ACÁ
    pass


# Subir a todos
# Sumale 'cuanto' al nivel de TODOS los Pokémon. Pista: UPDATE pokemon SET nivel = nivel + ?.
def subir_todos(conexion, cuanto):
    """Sumale 'cuanto' al nivel de cada Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Borrar uno
# Borrá un Pokémon por nombre. Pista: DELETE FROM pokemon WHERE nombre = ?.
def borrar(conexion, nombre):
    """Eliminá el Pokémon 'nombre'."""
    # TU CÓDIGO ACÁ
    pass


# Borrar a los débiles
# Borrá los Pokémon con nivel menor a 'umbral'. Pista: DELETE FROM pokemon WHERE nivel < ?.
def borrar_debiles(conexion, umbral):
    """Eliminá los que tengan nivel < umbral."""
    # TU CÓDIGO ACÁ
    pass
