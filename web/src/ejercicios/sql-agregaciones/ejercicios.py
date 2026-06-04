"""✏️ Ejercicios — SQL: agregaciones y GROUP BY

Resumir datos: COUNT, SUM, AVG, MAX, y agrupar con GROUP BY. Tabla 'pokemon'
(nombre, nivel, tipo). ✅ Corregir al terminar.
"""
import sqlite3


# Total (COUNT)
# Devolvé cuántos Pokémon hay (un int). Pista: SELECT COUNT(*) ... .fetchone()[0].
def total(conexion):
    """Devolvé la cantidad de Pokémon (int)."""
    # TU CÓDIGO ACÁ
    pass


# Promedio (AVG)
# Devolvé el nivel promedio de todos. Pista: SELECT AVG(nivel) ...
def nivel_promedio(conexion):
    """Devolvé el nivel promedio."""
    # TU CÓDIGO ACÁ
    pass


# Máximo (MAX)
# Devolvé el nivel más alto. Pista: SELECT MAX(nivel) ...
def nivel_maximo(conexion):
    """Devolvé el nivel máximo."""
    # TU CÓDIGO ACÁ
    pass


# Suma (SUM)
# Devolvé la suma de todos los niveles. Pista: SELECT SUM(nivel) ...
def suma_niveles(conexion):
    """Devolvé la suma de los niveles."""
    # TU CÓDIGO ACÁ
    pass


# Cuántos por tipo (GROUP BY)
# Devolvé un dict {tipo: cantidad}. Pista: SELECT tipo, COUNT(*) ... GROUP BY tipo.
# Ejemplo:  cuantos_por_tipo(con)  →  {"Electrico": 2, "Fuego": 1}
def cuantos_por_tipo(conexion):
    """Devolvé un dict {tipo: cantidad}."""
    # TU CÓDIGO ACÁ
    pass


# Promedio por tipo
# Devolvé un dict {tipo: promedio}. Pista: SELECT tipo, AVG(nivel) ... GROUP BY tipo.
def promedio_por_tipo(conexion):
    """Devolvé un dict {tipo: nivel promedio}."""
    # TU CÓDIGO ACÁ
    pass
