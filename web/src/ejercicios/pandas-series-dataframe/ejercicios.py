"""
✏️ Ejercicios — pandas: Series y DataFrame

Creamos y miramos tablas de datos (DataFrame) y columnas (Series).
"""
import pandas as pd


# 1) Convertí una lista en una Serie de pandas.
def crear_serie(valores):
    """Recibí [10, 20, 30] y devolvé una pd.Series con esos valores."""
    # TU CÓDIGO ACÁ
    pass


# 2) Creá una Serie con índices (nombres) propios.
def serie_con_indices(valores, nombres):
    """Recibí valores=[25, 90] y nombres=['Pikachu','Charizard'] y devolvé
    una Serie donde cada valor está etiquetado con su nombre."""
    # TU CÓDIGO ACÁ
    pass


# 3) Creá un DataFrame a partir de un diccionario de columnas.
def crear_pokedex(datos):
    """Recibí un dict como {'nombre': [...], 'nivel': [...]} y devolvé un DataFrame."""
    # TU CÓDIGO ACÁ
    pass


# 4) Devolvé la lista con los nombres de las columnas del DataFrame.
def nombres_columnas(df):
    """Devolvé list(df.columns)."""
    # TU CÓDIGO ACÁ
    pass


# 5) Devolvé una columna del DataFrame (como Serie).
def columna(df, nombre):
    """Devolvé la columna 'nombre' del df."""
    # TU CÓDIGO ACÁ
    pass


# 6) Devolvé cuántas filas tiene el DataFrame.
def cantidad_filas(df):
    """Devolvé la cantidad de filas (un int)."""
    # TU CÓDIGO ACÁ
    pass


# 7) Devolvé las primeras n filas del DataFrame. Usá .head().
def primeras_filas(df, n):
    """Devolvé df.head(n)."""
    # TU CÓDIGO ACÁ
    pass


# 8) Devolvé el promedio de una columna numérica.
def promedio_columna(df, col):
    """Devolvé la media de la columna 'col'."""
    # TU CÓDIGO ACÁ
    pass


# 9) Agregá una columna nueva al DataFrame y devolvé el DataFrame resultante.
def agregar_columna(df, nombre, valores):
    """Devolvé una COPIA del df con una columna nueva 'nombre' = valores."""
    # TU CÓDIGO ACÁ
    pass
