"""✏️ Ejercicios — pandas: Agrupar y combinar

Resumir datos con groupby y value_counts, y combinar tablas con merge.
DataFrame con columnas: nombre, tipo, nivel, hp. ✅ Corregir al terminar.
"""
import pandas as pd


# Cuántos por tipo
# Contá cuántos Pokémon hay de cada tipo. Pista: df["tipo"].value_counts().
# Ejemplo:  devuelve una Serie  Fuego→3, Agua→2, ...
def contar_por_tipo(df):
    """Devolvé una Serie: tipo → cantidad."""
    # TU CÓDIGO ACÁ
    pass


# Nivel promedio por tipo
# Calculá el nivel promedio de cada tipo. Pista: df.groupby("tipo")["nivel"].mean().
def nivel_promedio_por_tipo(df):
    """Devolvé una Serie: tipo → nivel promedio."""
    # TU CÓDIGO ACÁ
    pass


# Nivel máximo por tipo
# Calculá el nivel más alto de cada tipo. Pista: groupby + max().
def nivel_maximo_por_tipo(df):
    """Devolvé una Serie: tipo → nivel máximo."""
    # TU CÓDIGO ACÁ
    pass


# HP total por tipo
# Sumá el HP de cada tipo. Pista: groupby + sum().
def hp_total_por_tipo(df):
    """Devolvé una Serie: tipo → suma de hp."""
    # TU CÓDIGO ACÁ
    pass


# El tipo más común
# Devolvé el NOMBRE del tipo que más se repite. Pista: value_counts().idxmax().
# Ejemplo:  si hay más de Fuego que de otros  →  "Fuego"
def tipo_mas_comun(df):
    """Devolvé el tipo más repetido (str)."""
    # TU CÓDIGO ACÁ
    pass


# Combinar tablas (merge)
# Combiná dos DataFrames por una columna en común. Pista: pd.merge(df1, df2, on=col).
# Ejemplo:  combinar(pokemon, tipos, "tipo")  →  una tabla con info de ambas
def combinar(df1, df2, col):
    """Devolvé el merge de df1 y df2 usando 'col' como clave."""
    # TU CÓDIGO ACÁ
    pass


# Tipos populares
# Cantidad de Pokémon por tipo, pero SOLO de los tipos que tienen 2 o más.
# Pista: contá por tipo y filtrá la Serie con [serie >= 2].
def tipos_populares(df):
    """Devolvé una Serie tipo → cantidad, solo con los tipos de 2+ Pokémon."""
    # TU CÓDIGO ACÁ
    pass
