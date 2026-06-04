"""✏️ Ejercicios — pandas: Limpieza de datos

Datos faltantes (NaN), tipos, duplicados, renombrar y transformar columnas.
✅ Corregir al terminar.
"""
import pandas as pd


# Contar faltantes (NaN)
# Contá cuántos valores faltantes (NaN) hay en TODO el DataFrame. Devolvé un int.
# Pista: df.isna().sum().sum().
def contar_nulos(df):
    """Devolvé la cantidad total de NaN (int)."""
    # TU CÓDIGO ACÁ
    pass


# Rellenar con 0
# Reemplazá los NaN de una columna por 0. Devolvé una COPIA del df.
# Pista: df = df.copy(); df[col] = df[col].fillna(0).
def rellenar_ceros(df, col):
    """Devolvé una copia del df con los NaN de 'col' en 0."""
    # TU CÓDIGO ACÁ
    pass


# Quitar filas con NaN
# Eliminá las filas que tengan algún valor faltante. Pista: df.dropna().
def quitar_filas_nulas(df):
    """Devolvé el df sin filas con NaN."""
    # TU CÓDIGO ACÁ
    pass


# Serie a enteros
# Convertí los valores de una Serie a enteros. Pista: serie.astype(int).
# Ejemplo:  una Serie [25.0, 90.0]  →  [25, 90]
def a_entero(serie):
    """Devolvé la serie con sus valores como int."""
    # TU CÓDIGO ACÁ
    pass


# Sin duplicados
# Eliminá las filas repetidas del DataFrame. Pista: df.drop_duplicates().
def sin_duplicados(df):
    """Devolvé el df sin filas repetidas."""
    # TU CÓDIGO ACÁ
    pass


# Renombrar columna
# Cambiá el nombre de la columna 'viejo' por 'nuevo'. Devolvé una copia.
# Pista: df.rename(columns={viejo: nuevo}).
def renombrar(df, viejo, nuevo):
    """Devolvé el df con la columna renombrada."""
    # TU CÓDIGO ACÁ
    pass


# Textos a MAYÚSCULAS
# Pasá los textos de una Serie a mayúsculas. Pista: serie.str.upper().
# Ejemplo:  ["pikachu", "onix"]  →  ["PIKACHU", "ONIX"]
def a_mayusculas(serie):
    """Devolvé la serie de strings en mayúsculas."""
    # TU CÓDIGO ACÁ
    pass


# Aplicar una función
# Aplicá 'funcion' a cada valor de la Serie. Pista: serie.apply(funcion).
# Ejemplo:  aplicar(pd.Series([1, 2]), lambda x: x * 10)  →  [10, 20]
def aplicar(serie, funcion):
    """Devolvé la serie con 'funcion' aplicada a cada elemento."""
    # TU CÓDIGO ACÁ
    pass
