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


# Suma de una columna
# Devolvé la suma de los valores de la columna `col`.
def suma_columna(df, col):
    """Devolvé la suma de la columna."""
    # TU CÓDIGO ACÁ
    pass


# Máximo de una columna
# Devolvé el valor más grande de la columna `col`.
def maximo_columna(df, col):
    """Devolvé el máximo de la columna."""
    # TU CÓDIGO ACÁ
    pass


# Mínimo de una columna
# Devolvé el valor más chico de la columna `col`.
def minimo_columna(df, col):
    """Devolvé el mínimo de la columna."""
    # TU CÓDIGO ACÁ
    pass


# Columna a lista
# Devolvé los valores de la columna `col` como una lista de Python. Pista: .tolist().
def columna_a_lista(df, col):
    """Devolvé la columna como lista."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de columnas
# Devolvé cuántas columnas tiene el DataFrame.
def cantidad_columnas(df):
    """Devolvé la cantidad de columnas."""
    # TU CÓDIGO ACÁ
    pass


# ¿Existe la columna?
# Devolvé True si `col` es una columna del DataFrame.
def existe_columna(df, col):
    """Devolvé True si la columna existe."""
    # TU CÓDIGO ACÁ
    pass


# Contar filas donde
# Devolvé CUÁNTAS filas tienen la columna `col` con valor mayor que `n` (como int).
# Ejemplo:  con una columna "nivel" [25, 12, 18] y n=15  →  contar_donde(df, "nivel", 15)  →  2
def contar_donde(df, col, n):
    """Devolvé cuántas filas tienen col > n."""
    # TU CÓDIGO ACÁ
    pass


# Valores ordenados
# Devolvé los valores de la columna `col` ordenados de menor a mayor, como lista.
def valores_ordenados(df, col):
    """Devolvé los valores de col ordenados, como lista."""
    # TU CÓDIGO ACÁ
    pass


# Fila como diccionario
# Devolvé la fila número `i` como un diccionario {columna: valor}. Pista: df.iloc[i].to_dict().
def fila_como_dict(df, i):
    """Devolvé la fila i como dict."""
    # TU CÓDIGO ACÁ
    pass


# Renombrar columnas
# Devolvé la LISTA de nombres de columnas después de aplicar el renombre `mapa`
# (un dict {viejo: nuevo}). Pista: df.rename(columns=mapa).columns.
# Ejemplo:  con columnas ["nombre", "nivel"] y mapa {"nivel": "lvl"}  →  ["nombre", "lvl"]
def renombrar_columnas(df, mapa):
    """Devolvé los nombres de columnas tras renombrar."""
    # TU CÓDIGO ACÁ
    pass


# Mediana de una columna
# Devolvé la mediana de la columna `col`. Pista: .median().
def mediana_columna(df, col):
    """Devolvé la mediana de la columna."""
    # TU CÓDIGO ACÁ
    pass
