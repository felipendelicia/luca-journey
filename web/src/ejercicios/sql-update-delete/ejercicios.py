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


# Bajar a todos
# Restá `cuanto` al nivel de TODOS los Pokémon. Pista: UPDATE pokemon SET nivel = nivel - ?.
def bajar_todos(conexion, cuanto):
    """Bajá el nivel de todos en `cuanto`."""
    # TU CÓDIGO ACÁ
    pass


# Cambiar el tipo
# Cambiá el tipo del Pokémon `nombre` a `nuevo`. Pista: UPDATE ... SET tipo = ? WHERE nombre = ?.
def cambiar_tipo(conexion, nombre, nuevo):
    """Cambiá el tipo de ese Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Duplicar los niveles
# Multiplicá por 2 el nivel de todos. Pista: UPDATE ... SET nivel = nivel * 2.
def duplicar_niveles(conexion):
    """Duplicá el nivel de todos."""
    # TU CÓDIGO ACÁ
    pass


# Poner un nivel mínimo
# A los que tengan nivel menor que `minimo`, subiles el nivel a `minimo`.
# Pista: UPDATE ... SET nivel = ? WHERE nivel < ?.
def poner_nivel_minimo(conexion, minimo):
    """Subí al mínimo a los que estén por debajo."""
    # TU CÓDIGO ACÁ
    pass


# Borrar de un tipo
# Borrá todos los Pokémon de tipo `tipo`. Pista: DELETE FROM pokemon WHERE tipo = ?.
def borrar_de_tipo(conexion, tipo):
    """Borrá los de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Borrar todos
# Borrá TODOS los Pokémon de la tabla. Pista: DELETE FROM pokemon.
def borrar_todos(conexion):
    """Borrá todos los Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Subir a un tipo
# Sumá `cuanto` al nivel de los Pokémon de tipo `tipo`.
def subir_de_tipo(conexion, tipo, cuanto):
    """Subí el nivel a los de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Renombrar
# Cambiá el nombre del Pokémon `viejo` a `nuevo`.
def renombrar(conexion, viejo, nuevo):
    """Renombrá un Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Nivelar a todos
# Poné el nivel de TODOS en `valor`.
def nivelar(conexion, valor):
    """Poné el nivel de todos en valor."""
    # TU CÓDIGO ACÁ
    pass


# Borrar fuertes
# Borrá los Pokémon con nivel mayor que `umbral`.
def borrar_fuertes(conexion, umbral):
    """Borrá los de nivel > umbral."""
    # TU CÓDIGO ACÁ
    pass


# Limitar el nivel
# A los que tengan nivel mayor que `maximo`, bajales el nivel a `maximo`.
def limitar_nivel(conexion, maximo):
    """Limitá el nivel al máximo."""
    # TU CÓDIGO ACÁ
    pass


# Incrementar uno
# Sumá `cuanto` al nivel del Pokémon `nombre`.
def incrementar(conexion, nombre, cuanto):
    """Subí el nivel de un Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Cambiar el nivel de un tipo
# Poné el nivel de todos los Pokémon de tipo `tipo` en `valor`.
def cambiar_nivel_de_tipo(conexion, tipo, valor):
    """Poné el nivel de los de ese tipo en valor."""
    # TU CÓDIGO ACÁ
    pass


# Sumar a los débiles
# A los Pokémon con nivel menor que `umbral`, sumales `cuanto`.
def sumar_a_los_debiles(conexion, umbral, cuanto):
    """Sumá cuanto a los de nivel < umbral."""
    # TU CÓDIGO ACÁ
    pass


# Reemplazar un tipo
# Cambiá el tipo `viejo` por `nuevo` en todos los que lo tengan.
def reset_tipo(conexion, viejo, nuevo):
    """Reemplazá un tipo por otro."""
    # TU CÓDIGO ACÁ
    pass


# Borrar y contar
# Borrá los Pokémon de tipo `tipo` y devolvé CUÁNTOS borraste. Pista: cursor.rowcount.
def borrar_y_contar(conexion, tipo):
    """Borrá los de ese tipo y devolvé cuántos."""
    # TU CÓDIGO ACÁ
    pass
