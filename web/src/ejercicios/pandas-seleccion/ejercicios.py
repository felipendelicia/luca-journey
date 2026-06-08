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


# Nombres
# Devolvé la columna "nombre" como lista.
def nombres(df):
    """Devolvé los nombres como lista."""
    # TU CÓDIGO ACÁ
    pass


# Valor en una celda
# Devolvé el valor de la fila `fila`, columna `col`. Pista: df.iloc[fila][col].
def valor_en(df, fila, col):
    """Devolvé el valor de esa celda."""
    # TU CÓDIGO ACÁ
    pass


# Última fila
# Devolvé la última fila como diccionario.
def ultima_fila(df):
    """Devolvé la última fila como dict."""
    # TU CÓDIGO ACÁ
    pass


# El más débil
# Devolvé como diccionario la fila del Pokémon con menor "nivel". Pista: df["nivel"].idxmin().
def mas_debil(df):
    """Devolvé la fila del menor nivel, como dict."""
    # TU CÓDIGO ACÁ
    pass


# Nivel de un Pokémon
# Devolvé el "nivel" del Pokémon cuyo "nombre" sea `nombre`, o None si no está.
def nivel_de(df, nombre):
    """Devolvé el nivel de ese nombre, o None."""
    # TU CÓDIGO ACÁ
    pass


# ¿Existe el nombre?
# Devolvé True si hay una fila con ese "nombre".
def existe_nombre(df, nombre):
    """Devolvé True si está ese nombre."""
    # TU CÓDIGO ACÁ
    pass


# Primeros n nombres
# Devolvé los nombres de las primeras `n` filas, como lista.
def primeros_nombres(df, n):
    """Devolvé los primeros n nombres."""
    # TU CÓDIGO ACÁ
    pass


# Nombres ordenados
# Devolvé los nombres ordenados alfabéticamente, como lista.
def ordenar_nombres(df):
    """Devolvé los nombres ordenados."""
    # TU CÓDIGO ACÁ
    pass


# Contar de un tipo
# Devolvé cuántas filas tienen "tipo" igual a `tipo` (como int).
def contar_tipo(df, tipo):
    """Devolvé cuántos son de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Niveles entre lo y hi
# Devolvé los NOMBRES de los Pokémon con nivel entre `lo` y `hi` (ambos incluidos).
def niveles_entre(df, lo, hi):
    """Devolvé los nombres con nivel entre lo y hi."""
    # TU CÓDIGO ACÁ
    pass


# Top n niveles
# Devolvé los `n` niveles más altos, de mayor a menor, como lista.
# Ejemplo:  con niveles [25, 12, 18, 30] y n=2  →  top_niveles(df, 2)  →  [30, 25]
def top_niveles(df, n):
    """Devolvé los n niveles más altos."""
    # TU CÓDIGO ACÁ
    pass


# Nombres de un tipo
# Devolvé los NOMBRES de los Pokémon cuyo "tipo" sea `tipo`, como lista.
def nombres_de_tipo(df, tipo):
    """Devolvé los nombres de ese tipo."""
    # TU CÓDIGO ACÁ
    pass
