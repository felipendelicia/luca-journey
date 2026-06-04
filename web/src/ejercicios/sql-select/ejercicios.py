"""
✏️ Ejercicios — SQL: filtrar y ordenar

WHERE para filtrar, ORDER BY para ordenar, LIKE para buscar texto, LIMIT para cortar.
La tabla 'pokemon' tiene: nombre, nivel, tipo.
"""
import sqlite3


# 1) Nombres de los Pokémon de un tipo dado. Usá WHERE.
def de_tipo(conexion, tipo):
    """Devolvé una lista de nombres donde tipo = el pedido. Usá parámetros (?)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Nombres de los Pokémon con nivel >= mínimo, ordenados de mayor a menor nivel.
def fuertes(conexion, minimo):
    """WHERE nivel >= ? ORDER BY nivel DESC."""
    # TU CÓDIGO ACÁ
    pass


# 3) Todos los nombres ordenados por nivel descendente.
def ordenados_por_nivel(conexion):
    """ORDER BY nivel DESC."""
    # TU CÓDIGO ACÁ
    pass


# 4) Nombres que empiezan con una letra dada. Usá LIKE (ej: 'C%').
def empiezan_con(conexion, letra):
    """WHERE nombre LIKE ?  (pasale letra + '%')."""
    # TU CÓDIGO ACÁ
    pass


# 5) Los n Pokémon de mayor nivel (nombres). Usá ORDER BY ... LIMIT.
def top(conexion, n):
    """ORDER BY nivel DESC LIMIT ?."""
    # TU CÓDIGO ACÁ
    pass
