"""✏️ Ejercicios — pandas: Selección y filtrado

Elegir filas/columnas (loc/iloc), filtros booleanos y ordenamiento. Las funciones
reciben un DataFrame con columnas: nombre, nivel, tipo, hp. ✅ Corregir al terminar.
"""
import pandas as pd


# Fila por posición
# Devolvé la fila en la posición i (un entero). Pista: df.iloc[i].
# Ejemplo:  fila_por_posicion(df, 0)  →  la primera fila (como Serie)
def fila_por_posicion(df, i):
    """Devolvé df.iloc[i]."""
    # TU CÓDIGO ACÁ
    pass


# Filtrar por nivel
# Devolvé las filas con nivel mayor o igual al mínimo (filtro booleano).
# Ejemplo:  filtrar_nivel(df, 50)  →  solo los Pokémon de nivel 50 o más
def filtrar_nivel(df, minimo):
    """Devolvé el sub-DataFrame con nivel >= minimo."""
    # TU CÓDIGO ACÁ
    pass


# Filas de un tipo
# Devolvé las filas donde la columna 'tipo' es igual al 'tipo' dado.
# Ejemplo:  de_tipo(df, "Fuego")  →  solo los Pokémon de Fuego
def de_tipo(df, tipo):
    """Devolvé las filas de ese 'tipo'."""
    # TU CÓDIGO ACÁ
    pass


# Ordenar por nivel
# Devolvé el DataFrame ordenado por 'nivel', de mayor a menor.
# Pista: df.sort_values("nivel", ascending=False).
def ordenar_por_nivel(df):
    """Devolvé el df ordenado por 'nivel' descendente."""
    # TU CÓDIGO ACÁ
    pass


# Los más fuertes (nombres)
# Devolvé una LISTA (no una Serie) con los nombres que tienen nivel >= minimo.
# Pista: list(df[df["nivel"] >= minimo]["nombre"]).
# Ejemplo:  nombres_fuertes(df, 50)  →  ["Charizard", "Snorlax"]
def nombres_fuertes(df, minimo):
    """Devolvé una lista de nombres con nivel >= minimo."""
    # TU CÓDIGO ACÁ
    pass


# Solo estas columnas
# 'cols' es una lista de nombres de columna. Devolvé el DataFrame solo con esas columnas.
# Ejemplo:  solo_columnas(df, ["nombre", "nivel"])  →  tabla de 2 columnas
def solo_columnas(df, cols):
    """Devolvé el df con solo las columnas pedidas."""
    # TU CÓDIGO ACÁ
    pass


# Quitar una columna
# Devolvé una copia del DataFrame SIN la columna indicada (sin modificar el original).
# Pista: df.drop(columns=[col]).
def quitar_columna(df, col):
    """Devolvé una copia del df sin la columna 'col'."""
    # TU CÓDIGO ACÁ
    pass


# El más fuerte
# Devolvé el NOMBRE del Pokémon con el nivel más alto. Pista: df["nivel"].idxmax().
# Ejemplo:  el de nivel más alto es Charizard  →  el_mas_fuerte(df)  →  "Charizard"
def el_mas_fuerte(df):
    """Devolvé el nombre (str) de la fila con mayor 'nivel'."""
    # TU CÓDIGO ACÁ
    pass
