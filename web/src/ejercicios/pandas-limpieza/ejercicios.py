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


# Sacar espacios
# Devolvé la Serie con cada texto sin espacios al borde. Pista: .str.strip().
def sacar_espacios(serie):
    """Devolvé la serie sin espacios al borde."""
    # TU CÓDIGO ACÁ
    pass


# A minúsculas
# Devolvé la Serie con cada texto en minúsculas. Pista: .str.lower().
def a_minusculas(serie):
    """Devolvé la serie en minúsculas."""
    # TU CÓDIGO ACÁ
    pass


# Reemplazar un valor
# Devolvé la Serie con cada `viejo` cambiado por `nuevo`. Pista: .replace(viejo, nuevo).
def reemplazar_valor(serie, viejo, nuevo):
    """Devolvé la serie con viejo cambiado por nuevo."""
    # TU CÓDIGO ACÁ
    pass


# Contar únicos
# Devolvé cuántos valores DISTINTOS hay en la Serie (como int). Pista: .nunique().
def contar_unicos(serie):
    """Devolvé cuántos valores distintos hay."""
    # TU CÓDIGO ACÁ
    pass


# Valores únicos
# Devolvé los valores distintos ORDENADOS, como lista.
def valores_unicos(serie):
    """Devolvé los valores distintos, ordenados."""
    # TU CÓDIGO ACÁ
    pass


# Promedio sin nulos
# Devolvé el promedio de la Serie (pandas ignora los nulos solo). Pista: .mean().
# Ejemplo:  con valores [2, None, 4]  →  promedio_sin_nulos(serie)  →  3.0
def promedio_sin_nulos(serie):
    """Devolvé el promedio (ignorando nulos)."""
    # TU CÓDIGO ACÁ
    pass


# Contar un valor
# Devolvé cuántas veces aparece `v` en la Serie (como int).
def contar_valor(serie, v):
    """Devolvé cuántas veces está v."""
    # TU CÓDIGO ACÁ
    pass


# El más frecuente
# Devolvé el valor que más se repite. Pista: .mode()[0].
def mas_frecuente(serie):
    """Devolvé el valor más frecuente."""
    # TU CÓDIGO ACÁ
    pass


# Capitalizar
# Devolvé la Serie con cada texto en formato Capitalizado (primera mayúscula). Pista: .str.capitalize().
def capitalizar(serie):
    """Devolvé la serie capitalizada."""
    # TU CÓDIGO ACÁ
    pass


# Columnas con nulos
# Devolvé una lista con los nombres de las columnas que tienen AL MENOS un valor nulo.
def columnas_con_nulos(df):
    """Devolvé las columnas que tienen nulos."""
    # TU CÓDIGO ACÁ
    pass


# Normalizar texto
# Devolvé la Serie con cada texto SIN espacios al borde Y en minúsculas.
# Ejemplo:  con [" Pikachu ", "ONIX"]  →  ["pikachu", "onix"]
def normalizar_texto(serie):
    """Devolvé la serie sin espacios y en minúsculas."""
    # TU CÓDIGO ACÁ
    pass


# Longitud de cada texto
# Devolvé una lista con la cantidad de caracteres de cada texto. Pista: .str.len().
def longitud_textos(serie):
    """Devolvé el largo de cada texto, como lista."""
    # TU CÓDIGO ACÁ
    pass
