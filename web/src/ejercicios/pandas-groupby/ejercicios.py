"""
✏️ Ejercicios — pandas: Agrupar y combinar

Resumir datos con groupby y value_counts, y combinar tablas con merge.
DataFrame con columnas: nombre, tipo, nivel, hp.
"""
import pandas as pd


# 1) Contá cuántos Pokémon hay de cada tipo. Usá value_counts.
def contar_por_tipo(df):
    """Devolvé una Serie: tipo -> cantidad."""
    # TU CÓDIGO ACÁ
    pass


# 2) Promedio de nivel por tipo. Usá groupby.
def nivel_promedio_por_tipo(df):
    """Devolvé una Serie: tipo -> nivel promedio."""
    # TU CÓDIGO ACÁ
    pass


# 3) Nivel máximo por tipo.
def nivel_maximo_por_tipo(df):
    """Devolvé una Serie: tipo -> nivel máximo."""
    # TU CÓDIGO ACÁ
    pass


# 4) HP total por tipo.
def hp_total_por_tipo(df):
    """Devolvé una Serie: tipo -> suma de hp."""
    # TU CÓDIGO ACÁ
    pass


# 5) ¿Cuál es el tipo más común? Devolvé el nombre del tipo (str).
def tipo_mas_comun(df):
    """Devolvé el tipo que más se repite. Pista: value_counts().idxmax()."""
    # TU CÓDIGO ACÁ
    pass


# 6) Combiná dos DataFrames por una columna en común. Usá pd.merge.
def combinar(df1, df2, col):
    """Devolvé el merge de df1 y df2 usando 'col' como clave."""
    # TU CÓDIGO ACÁ
    pass


# 7) Cantidad de Pokémon por tipo, pero solo de los tipos con 2 o más.
def tipos_populares(df):
    """Devolvé una Serie tipo -> cantidad, solo con los tipos que tienen 2+ Pokémon."""
    # TU CÓDIGO ACÁ
    pass
