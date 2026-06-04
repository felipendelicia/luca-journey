"""
✏️ Ejercicios — Análisis integrador

Un mini-análisis de punta a punta sobre una Pokédex: cargar, limpiar,
resumir y sacar conclusiones. Junta todo lo de la región Johto.
"""
import pandas as pd


# 1) Cargá los datos (un dict de columnas) en un DataFrame.
def cargar(datos):
    """Devolvé un DataFrame a partir del dict 'datos'."""
    # TU CÓDIGO ACÁ
    pass


# 2) Limpiá: sacá las filas con datos faltantes (NaN) y reseteá el índice.
def limpiar(df):
    """Devolvé el df sin filas con NaN, con el índice reordenado (0,1,2...).
    Pista: .dropna().reset_index(drop=True)."""
    # TU CÓDIGO ACÁ
    pass


# 3) ¿Cuántos Pokémon hay en la tabla?
def cantidad(df):
    """Devolvé la cantidad de filas (int)."""
    # TU CÓDIGO ACÁ
    pass


# 4) ¿Cuál es el tipo más común?
def tipo_mas_comun(df):
    """Devolvé el tipo (str) que más aparece."""
    # TU CÓDIGO ACÁ
    pass


# 5) Nivel promedio de toda la Pokédex.
def nivel_promedio(df):
    """Devolvé el promedio de la columna 'nivel'."""
    # TU CÓDIGO ACÁ
    pass


# 6) Devolvé los n Pokémon de mayor nivel (DataFrame).
def top_n(df, n):
    """Ordená por nivel descendente y devolvé las primeras n filas."""
    # TU CÓDIGO ACÁ
    pass


# 7) Nivel promedio por tipo (Serie tipo -> promedio).
def promedio_por_tipo(df):
    """Devolvé una Serie con el nivel promedio de cada tipo."""
    # TU CÓDIGO ACÁ
    pass


# 8) Devolvé el NOMBRE del Pokémon de mayor nivel dentro de un tipo dado.
def campeon_del_tipo(df, tipo):
    """Filtrá por 'tipo' y devolvé el nombre del de mayor nivel."""
    # TU CÓDIGO ACÁ
    pass
