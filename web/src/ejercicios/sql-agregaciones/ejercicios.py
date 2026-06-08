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


# Nivel mínimo
# Devolvé el nivel más bajo. Pista: SELECT MIN(nivel) ...
def nivel_minimo(conexion):
    """Devolvé el nivel mínimo."""
    # TU CÓDIGO ACÁ
    pass


# Cuántos de un tipo
# Devolvé cuántos Pokémon hay de tipo `tipo`. Pista: COUNT(*) ... WHERE tipo = ?.
def cuantos_de_tipo(conexion, tipo):
    """Devolvé cuántos son de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Suma de nivel por tipo
# Devolvé un dict tipo → suma de niveles. Pista: SELECT tipo, SUM(nivel) ... GROUP BY tipo.
def suma_por_tipo(conexion):
    """Devolvé un dict tipo → suma de niveles."""
    # TU CÓDIGO ACÁ
    pass


# Máximo por tipo
# Devolvé un dict tipo → nivel máximo. Pista: SELECT tipo, MAX(nivel) ... GROUP BY tipo.
def maximo_por_tipo(conexion):
    """Devolvé un dict tipo → nivel máximo."""
    # TU CÓDIGO ACÁ
    pass


# El tipo más numeroso
# Devolvé el tipo que tiene MÁS Pokémon. Pista: GROUP BY tipo ORDER BY COUNT(*) DESC LIMIT 1.
def tipo_mas_numeroso(conexion):
    """Devolvé el tipo con más Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Nivel total de un tipo
# Devolvé la suma de niveles de los Pokémon de tipo `tipo`. Pista: SUM(nivel) ... WHERE tipo = ?.
def nivel_total_de_tipo(conexion, tipo):
    """Devolvé la suma de niveles de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de tipos
# Devolvé cuántos tipos DISTINTOS hay. Pista: SELECT COUNT(DISTINCT tipo) ...
def cantidad_tipos(conexion):
    """Devolvé cuántos tipos distintos hay."""
    # TU CÓDIGO ACÁ
    pass


# Rango de nivel
# Devolvé la diferencia entre el nivel máximo y el mínimo. Pista: MAX(nivel) - MIN(nivel).
def rango_nivel(conexion):
    """Devolvé máximo - mínimo de nivel."""
    # TU CÓDIGO ACÁ
    pass


# Cuántos por encima de un nivel
# Devolvé cuántos Pokémon tienen nivel mayor que `n`.
def cuantos_arriba_de(conexion, n):
    """Devolvé cuántos tienen nivel > n."""
    # TU CÓDIGO ACÁ
    pass


# Promedio de un tipo
# Devolvé el nivel promedio de los Pokémon de tipo `tipo`. Pista: AVG(nivel) ... WHERE tipo = ?.
def promedio_de_tipo(conexion, tipo):
    """Devolvé el promedio de nivel de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Mínimo por tipo
# Devolvé un dict tipo → nivel mínimo. Pista: SELECT tipo, MIN(nivel) ... GROUP BY tipo.
def minimo_por_tipo(conexion):
    """Devolvé un dict tipo → nivel mínimo."""
    # TU CÓDIGO ACÁ
    pass


# El más fuerte
# Devolvé el NOMBRE del Pokémon de mayor nivel.
def el_mas_fuerte(conexion):
    """Devolvé el nombre del de mayor nivel."""
    # TU CÓDIGO ACÁ
    pass


# ¿Hay de ese tipo?
# Devolvé True si hay al menos un Pokémon de tipo `tipo`.
def hay_de_tipo(conexion, tipo):
    """Devolvé True si hay alguno de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Conteo por tipo ordenado
# Devolvé una lista de tuplas (tipo, cantidad) ordenada de MÁS a menos (y por tipo si empatan).
# Pista: SELECT tipo, COUNT(*) ... GROUP BY tipo ORDER BY COUNT(*) DESC, tipo.
def conteo_por_tipo_ordenado(conexion):
    """Devolvé (tipo, cantidad) ordenado por cantidad (desc)."""
    # TU CÓDIGO ACÁ
    pass
