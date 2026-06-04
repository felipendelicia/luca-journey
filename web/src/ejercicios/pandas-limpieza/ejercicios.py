"""
✏️ Ejercicios — pandas: Limpieza de datos

Datos faltantes (NaN), tipos, duplicados, renombrar y transformar columnas.
"""
import pandas as pd


# 1) Contá cuántos valores faltantes (NaN) hay en TODO el DataFrame. Devolvé un int.
def contar_nulos(df):
    """Usá df.isna().sum().sum(). Devolvé un int."""
    # TU CÓDIGO ACÁ
    pass


# 2) Rellená los NaN de una columna con 0. Devolvé una copia del df.
def rellenar_ceros(df, col):
    """Devolvé una copia del df con los NaN de 'col' reemplazados por 0."""
    # TU CÓDIGO ACÁ
    pass


# 3) Eliminá las filas que tengan algún NaN.
def quitar_filas_nulas(df):
    """Devolvé el df sin filas con NaN. Usá .dropna()."""
    # TU CÓDIGO ACÁ
    pass


# 4) Convertí una Serie a enteros. Usá .astype(int).
def a_entero(serie):
    """Devolvé la serie con sus valores como int."""
    # TU CÓDIGO ACÁ
    pass


# 5) Eliminá filas duplicadas del DataFrame.
def sin_duplicados(df):
    """Devolvé el df sin filas repetidas. Usá .drop_duplicates()."""
    # TU CÓDIGO ACÁ
    pass


# 6) Renombrá una columna. Devolvé una copia del df.
def renombrar(df, viejo, nuevo):
    """Cambiá el nombre de la columna 'viejo' por 'nuevo'. Usá .rename(columns=...)."""
    # TU CÓDIGO ACÁ
    pass


# 7) Pasá los textos de una Serie a MAYÚSCULAS. Usá .str.upper().
def a_mayusculas(serie):
    """Devolvé la serie de strings en mayúsculas."""
    # TU CÓDIGO ACÁ
    pass


# 8) Aplicá una función a cada valor de una Serie. Usá .apply().
def aplicar(serie, funcion):
    """Devolvé la serie con 'funcion' aplicada a cada elemento."""
    # TU CÓDIGO ACÁ
    pass
