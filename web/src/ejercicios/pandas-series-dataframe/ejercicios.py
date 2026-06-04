"""✏️ Ejercicios — pandas: Series y DataFrame

Crear y mirar tablas (DataFrame) y columnas (Series), con pandas (importado como pd).
✅ Corregir al terminar.
"""
import pandas as pd


# Lista a Serie
# Convertí una lista en una Serie de pandas. Pista: pd.Series(...).
# Ejemplo:  crear_serie([10, 20, 30])  →  una Serie con 10, 20, 30
def crear_serie(valores):
    """Devolvé una pd.Series con los valores."""
    # TU CÓDIGO ACÁ
    pass


# Serie con etiquetas
# Creá una Serie donde cada valor lleva su nombre como índice. Pista: pd.Series(valores, index=nombres).
# Ejemplo:  serie_con_indices([25, 90], ["Pikachu", "Charizard"])  →  Pikachu→25, Charizard→90
def serie_con_indices(valores, nombres):
    """Devolvé una Serie con 'nombres' como índice."""
    # TU CÓDIGO ACÁ
    pass


# Crear un DataFrame
# Armá un DataFrame a partir de un diccionario de columnas. Pista: pd.DataFrame(datos).
# Ejemplo:  crear_pokedex({"nombre": ["Pikachu"], "nivel": [25]})  →  una tabla de 1 fila
def crear_pokedex(datos):
    """Devolvé un DataFrame a partir del dict de columnas."""
    # TU CÓDIGO ACÁ
    pass


# Nombres de columnas
# Devolvé la lista con los nombres de las columnas. Pista: list(df.columns).
# Ejemplo:  un df con columnas nombre y nivel  →  ["nombre", "nivel"]
def nombres_columnas(df):
    """Devolvé list(df.columns)."""
    # TU CÓDIGO ACÁ
    pass


# Una columna
# Devolvé una columna del DataFrame (como Serie). Pista: df[nombre].
# Ejemplo:  columna(df, "nivel")  →  la columna 'nivel'
def columna(df, nombre):
    """Devolvé la columna 'nombre'."""
    # TU CÓDIGO ACÁ
    pass


# ¿Cuántas filas?
# Devolvé cuántas filas tiene el DataFrame (un int). Pista: len(df).
# Ejemplo:  un df de 5 filas  →  5
def cantidad_filas(df):
    """Devolvé la cantidad de filas (int)."""
    # TU CÓDIGO ACÁ
    pass


# Primeras filas
# Devolvé las primeras n filas. Pista: df.head(n).
# Ejemplo:  primeras_filas(df, 3)  →  las 3 primeras filas
def primeras_filas(df, n):
    """Devolvé df.head(n)."""
    # TU CÓDIGO ACÁ
    pass


# Promedio de una columna
# Devolvé el promedio de una columna numérica. Pista: df[col].mean().
# Ejemplo:  niveles 10, 20, 30  →  promedio_columna(df, "nivel")  →  20.0
def promedio_columna(df, col):
    """Devolvé la media de la columna 'col'."""
    # TU CÓDIGO ACÁ
    pass


# Agregar una columna
# Devolvé una COPIA del DataFrame con una columna nueva 'nombre' = valores.
# Pista: df = df.copy(); df[nombre] = valores; return df.
def agregar_columna(df, nombre, valores):
    """Devolvé una copia del df con la columna nueva."""
    # TU CÓDIGO ACÁ
    pass
