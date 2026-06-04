"""✏️ Ejercicios — SQL: relaciones y JOIN

Los datos suelen estar en VARIAS tablas relacionadas. JOIN las combina. Tenés dos tablas:
  pokemon(nombre, tipo)  ·  tipos(tipo, debilidad)   (relacionadas por 'tipo')
✅ Corregir al terminar.
"""
import sqlite3


# Combinar con JOIN
# Devolvé pares (nombre, debilidad) combinando ambas tablas.
# Pista: SELECT p.nombre, t.debilidad FROM pokemon p JOIN tipos t ON p.tipo = t.tipo.
# Ejemplo:  [("Charizard", "Agua"), ("Blastoise", "Planta")]
def con_debilidad(conexion):
    """Devolvé una lista de tuplas (nombre, debilidad)."""
    # TU CÓDIGO ACÁ
    pass


# Debilidad de uno
# Devolvé la debilidad de UN Pokémon (por su nombre). Usá JOIN + WHERE.
# Ejemplo:  debilidad_de(con, "Charizard")  →  "Agua"
def debilidad_de(conexion, nombre):
    """Devolvé la debilidad del tipo de ese Pokémon (str)."""
    # TU CÓDIGO ACÁ
    pass


# Débiles a un elemento
# Devolvé los NOMBRES de los Pokémon cuyo tipo es débil a 'elemento'.
# Pista: JOIN + WHERE t.debilidad = ?.
# Ejemplo:  debiles_a(con, "Agua")  →  ["Charizard", "Vulpix"]
def debiles_a(conexion, elemento):
    """Devolvé los nombres de los débiles a 'elemento'."""
    # TU CÓDIGO ACÁ
    pass
