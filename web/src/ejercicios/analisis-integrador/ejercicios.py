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


# Mediana de nivel
# Devolvé la mediana de la columna "nivel".
def mediana_nivel(df):
    """Devolvé la mediana de los niveles."""
    # TU CÓDIGO ACÁ
    pass


# Proporción de un tipo
# Devolvé la FRACCIÓN de Pokémon que son del tipo `tipo` (float entre 0 y 1).
# Ejemplo:  con 2 de "agua" de 5  →  proporcion_tipo(df, "agua")  →  0.4
def proporcion_tipo(df, tipo):
    """Devolvé la fracción de Pokémon de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Nombres del top n
# Devolvé los NOMBRES de los `n` Pokémon de mayor nivel, de mayor a menor.
def nombres_top(df, n):
    """Devolvé los nombres de los n de mayor nivel."""
    # TU CÓDIGO ACÁ
    pass


# Tipos únicos
# Devolvé una lista ORDENADA con los tipos distintos.
def tipos_unicos(df):
    """Devolvé los tipos distintos, ordenados."""
    # TU CÓDIGO ACÁ
    pass


# Filtrar fuertes
# Devolvé los NOMBRES de los Pokémon con nivel mayor o igual a `minimo`.
def filtrar_fuertes(df, minimo):
    """Devolvé los nombres con nivel >= minimo."""
    # TU CÓDIGO ACÁ
    pass


# Rango de niveles
# Devolvé la diferencia entre el nivel máximo y el mínimo (como int).
def rango_niveles(df):
    """Devolvé nivel máximo - mínimo."""
    # TU CÓDIGO ACÁ
    pass


# Tipo con mayor promedio
# Devolvé el tipo cuyo nivel PROMEDIO sea el más alto.
def tipo_con_mayor_promedio(df):
    """Devolvé el tipo de mayor nivel promedio."""
    # TU CÓDIGO ACÁ
    pass


# Contar por rango de nivel
# Devolvé cuántos Pokémon tienen nivel entre `lo` y `hi` (ambos incluidos), como int.
def contar_por_rango(df, lo, hi):
    """Devolvé cuántos tienen nivel entre lo y hi."""
    # TU CÓDIGO ACÁ
    pass


# Nivel total
# Devolvé la suma de todos los niveles.
def nivel_total(df):
    """Devolvé la suma de los niveles."""
    # TU CÓDIGO ACÁ
    pass


# ¿Hay alguno fuerte?
# Devolvé True si algún Pokémon tiene nivel mayor o igual a `umbral`.
def hay_fuertes(df, umbral):
    """Devolvé True si alguno alcanza el umbral."""
    # TU CÓDIGO ACÁ
    pass


# Tabla resumen
# Devolvé un dict con "total" (cantidad de filas), "tipos" (cantidad de tipos distintos) y
# "nivel_total" (suma de niveles).
# Ejemplo:  {"total": 5, "tipos": 3, "nivel_total": 130}
def tabla_resumen(df):
    """Devolvé un dict resumen."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad por tipo
# Devolvé un dict tipo → cantidad de Pokémon de ese tipo.
def cantidad_por_tipo(df):
    """Devolvé un dict tipo → cantidad."""
    # TU CÓDIGO ACÁ
    pass
