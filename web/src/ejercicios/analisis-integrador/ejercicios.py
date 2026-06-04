"""✏️ Ejercicios — Análisis integrador

Un mini-análisis de punta a punta sobre una Pokédex: cargar, limpiar, resumir y
sacar conclusiones. Junta todo lo de Johto. ✅ Corregir al terminar.
"""
import pandas as pd


# Cargar la Pokédex
# Convertí un dict de columnas en un DataFrame. Pista: pd.DataFrame(datos).
def cargar(datos):
    """Devolvé un DataFrame a partir de 'datos'."""
    # TU CÓDIGO ACÁ
    pass


# Limpiar los datos
# Sacá las filas con datos faltantes (NaN) y reordená el índice (0, 1, 2...).
# Pista: df.dropna().reset_index(drop=True).
def limpiar(df):
    """Devolvé el df sin NaN y con el índice reordenado."""
    # TU CÓDIGO ACÁ
    pass


# ¿Cuántos hay?
# Devolvé cuántos Pokémon tiene la tabla (int).
def cantidad(df):
    """Devolvé la cantidad de filas (int)."""
    # TU CÓDIGO ACÁ
    pass


# Tipo más común
# Devolvé el tipo (str) que más aparece. Pista: value_counts().idxmax().
def tipo_mas_comun(df):
    """Devolvé el tipo que más aparece."""
    # TU CÓDIGO ACÁ
    pass


# Nivel promedio
# Devolvé el promedio de la columna 'nivel' de toda la Pokédex.
def nivel_promedio(df):
    """Devolvé el promedio de 'nivel'."""
    # TU CÓDIGO ACÁ
    pass


# Top N por nivel
# Ordená por nivel de mayor a menor y devolvé las primeras n filas (DataFrame).
# Ejemplo:  top_n(df, 3)  →  los 3 de mayor nivel
def top_n(df, n):
    """Devolvé las n filas de mayor 'nivel'."""
    # TU CÓDIGO ACÁ
    pass


# Promedio por tipo
# Devolvé una Serie con el nivel promedio de cada tipo. Pista: groupby + mean.
def promedio_por_tipo(df):
    """Devolvé una Serie: tipo → nivel promedio."""
    # TU CÓDIGO ACÁ
    pass


# Campeón del tipo
# Filtrá por 'tipo' y devolvé el NOMBRE del Pokémon de mayor nivel de ese tipo.
# Ejemplo:  campeon_del_tipo(df, "Fuego")  →  "Charizard"
def campeon_del_tipo(df, tipo):
    """Devolvé el nombre del de mayor nivel dentro de 'tipo'."""
    # TU CÓDIGO ACÁ
    pass
