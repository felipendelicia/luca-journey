"""
✏️ Ejercicios — SQL: relaciones y JOIN

Los datos suelen estar en VARIAS tablas relacionadas. JOIN las combina.
Tenés dos tablas:
  pokemon(nombre, tipo)
  tipos(tipo, debilidad)     -- a qué es débil cada tipo
Se relacionan por la columna 'tipo'.
"""
import sqlite3


# 1) Devolvé pares (nombre_pokemon, debilidad) combinando ambas tablas con JOIN.
def con_debilidad(conexion):
    """SELECT p.nombre, t.debilidad FROM pokemon p JOIN tipos t ON p.tipo = t.tipo.
    Devolvé una lista de tuplas (nombre, debilidad)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Devolvé la debilidad de UN Pokémon (por su nombre). Usá JOIN + WHERE.
def debilidad_de(conexion, nombre):
    """Devolvé un string (la debilidad del tipo de ese Pokémon)."""
    # TU CÓDIGO ACÁ
    pass


# 3) Nombres de los Pokémon cuyo tipo es débil a 'elemento'.
def debiles_a(conexion, elemento):
    """JOIN + WHERE t.debilidad = ?. Devolvé una lista de nombres."""
    # TU CÓDIGO ACÁ
    pass
