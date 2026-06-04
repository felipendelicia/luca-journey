"""
✏️ Ejercicios — pandas: Selección y filtrado

Elegir filas/columnas con loc/iloc, filtros booleanos y ordenamiento.
Las funciones reciben un DataFrame con columnas: nombre, nivel, tipo, hp.
"""
import pandas as pd


# 1) Devolvé la fila en la posición i (entero). Usá .iloc.
def fila_por_posicion(df, i):
    """Devolvé df.iloc[i] (una Serie)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Devolvé las filas con nivel mayor o igual al mínimo (filtro booleano).
def filtrar_nivel(df, minimo):
    """Devolvé el sub-DataFrame con nivel >= minimo."""
    # TU CÓDIGO ACÁ
    pass


# 3) Devolvé las filas de un tipo dado.
def de_tipo(df, tipo):
    """Devolvé las filas donde la columna 'tipo' es igual a tipo."""
    # TU CÓDIGO ACÁ
    pass


# 4) Ordená el DataFrame por nivel, de mayor a menor.
def ordenar_por_nivel(df):
    """Devolvé el df ordenado por 'nivel' descendente."""
    # TU CÓDIGO ACÁ
    pass


# 5) Devolvé la lista de nombres con nivel >= minimo.
def nombres_fuertes(df, minimo):
    """Devolvé una lista (no una Serie) con los nombres que cumplen nivel >= minimo."""
    # TU CÓDIGO ACÁ
    pass


# 6) Devolvé un DataFrame solo con las columnas pedidas.
def solo_columnas(df, cols):
    """cols es una lista de nombres de columna. Devolvé df con esas columnas."""
    # TU CÓDIGO ACÁ
    pass


# 7) Devolvé el DataFrame sin la columna indicada (sin modificar el original).
def quitar_columna(df, col):
    """Devolvé una copia del df sin la columna 'col'. Usá .drop(columns=...)."""
    # TU CÓDIGO ACÁ
    pass


# 8) Devolvé el NOMBRE del Pokémon con el nivel más alto. Usá idxmax.
def el_mas_fuerte(df):
    """Devolvé el nombre (str) de la fila con mayor 'nivel'."""
    # TU CÓDIGO ACÁ
    pass
