"""✏️ Ejercicios — SQL: filtrar y ordenar

WHERE para filtrar, ORDER BY para ordenar, LIKE para buscar texto, LIMIT para cortar.
La tabla 'pokemon' tiene: nombre, nivel, tipo. ✅ Corregir al terminar.
"""
import sqlite3


# Filtrar por tipo
# Devolvé los nombres de los Pokémon de un tipo dado. Usá WHERE con parámetro (?).
# Ejemplo:  de_tipo(con, "Fuego")  →  ["Charizard", "Vulpix"]
def de_tipo(conexion, tipo):
    """Devolvé los nombres donde tipo = el pedido."""
    # TU CÓDIGO ACÁ
    pass


# Los fuertes, ordenados
# Nombres con nivel >= mínimo, ordenados de mayor a menor nivel.
# Pista: WHERE nivel >= ? ORDER BY nivel DESC.
# Ejemplo:  fuertes(con, 50)  →  ["Charizard", "Snorlax"]
def fuertes(conexion, minimo):
    """Devolvé los nombres con nivel >= mínimo, de mayor a menor."""
    # TU CÓDIGO ACÁ
    pass


# Ordenar por nivel
# Devolvé todos los nombres ordenados por nivel descendente. Pista: ORDER BY nivel DESC.
def ordenados_por_nivel(conexion):
    """Devolvé los nombres ordenados por nivel (mayor a menor)."""
    # TU CÓDIGO ACÁ
    pass


# Empiezan con…
# Devolvé los nombres que empiezan con una letra dada. Pista: WHERE nombre LIKE ? (letra + '%').
# Ejemplo:  empiezan_con(con, "C")  →  ["Charizard", "Charmander"]
def empiezan_con(conexion, letra):
    """Devolvé los nombres que empiezan con 'letra'."""
    # TU CÓDIGO ACÁ
    pass


# Top n
# Devolvé los n Pokémon de mayor nivel (nombres). Pista: ORDER BY nivel DESC LIMIT ?.
# Ejemplo:  top(con, 2)  →  los 2 de mayor nivel
def top(conexion, n):
    """Devolvé los nombres de los n de mayor nivel."""
    # TU CÓDIGO ACÁ
    pass
