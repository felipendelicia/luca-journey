"""
✏️ Ejercicios — SQL: agregaciones y GROUP BY

Resumir datos: COUNT, SUM, AVG, MAX, y agrupar con GROUP BY.
Tabla 'pokemon' (nombre, nivel, tipo).
"""
import sqlite3


# 1) ¿Cuántos Pokémon hay? Usá COUNT(*). Devolvé un int.
def total(conexion):
    """SELECT COUNT(*) ... .fetchone()[0]."""
    # TU CÓDIGO ACÁ
    pass


# 2) Nivel promedio de todos. Usá AVG(nivel). Devolvé el número.
def nivel_promedio(conexion):
    """SELECT AVG(nivel) ..."""
    # TU CÓDIGO ACÁ
    pass


# 3) Nivel máximo. Usá MAX(nivel).
def nivel_maximo(conexion):
    """SELECT MAX(nivel) ..."""
    # TU CÓDIGO ACÁ
    pass


# 4) Suma de todos los niveles. Usá SUM(nivel).
def suma_niveles(conexion):
    """SELECT SUM(nivel) ..."""
    # TU CÓDIGO ACÁ
    pass


# 5) ¿Cuántos Pokémon hay de cada tipo? Devolvé un dict {tipo: cantidad}.
def cuantos_por_tipo(conexion):
    """GROUP BY tipo. Armá un dict a partir de SELECT tipo, COUNT(*) ... GROUP BY tipo."""
    # TU CÓDIGO ACÁ
    pass


# 6) Nivel promedio por tipo. Devolvé un dict {tipo: promedio}.
def promedio_por_tipo(conexion):
    """SELECT tipo, AVG(nivel) ... GROUP BY tipo."""
    # TU CÓDIGO ACÁ
    pass
