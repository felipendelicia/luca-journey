"""✏️ Ejercicios — pandas: Agrupar y combinar

Resumir datos con groupby y value_counts, y combinar tablas con merge.
DataFrame con columnas: nombre, tipo, nivel, hp. ✅ Corregir al terminar.
"""
import pandas as pd


# Cuántos por tipo
# Contá cuántos Pokémon hay de cada tipo. Pista: df["tipo"].value_counts().
# Ejemplo:  devuelve una Serie  Fuego→3, Agua→2, ...
def contar_por_tipo(df):
    """Devolvé una Serie: tipo → cantidad."""
    # TU CÓDIGO ACÁ
    pass


# Nivel promedio por tipo
# Calculá el nivel promedio de cada tipo. Pista: df.groupby("tipo")["nivel"].mean().
def nivel_promedio_por_tipo(df):
    """Devolvé una Serie: tipo → nivel promedio."""
    # TU CÓDIGO ACÁ
    pass


# Nivel máximo por tipo
# Calculá el nivel más alto de cada tipo. Pista: groupby + max().
def nivel_maximo_por_tipo(df):
    """Devolvé una Serie: tipo → nivel máximo."""
    # TU CÓDIGO ACÁ
    pass


# HP total por tipo
# Sumá el HP de cada tipo. Pista: groupby + sum().
def hp_total_por_tipo(df):
    """Devolvé una Serie: tipo → suma de hp."""
    # TU CÓDIGO ACÁ
    pass


# El tipo más común
# Devolvé el NOMBRE del tipo que más se repite. Pista: value_counts().idxmax().
# Ejemplo:  si hay más de Fuego que de otros  →  "Fuego"
def tipo_mas_comun(df):
    """Devolvé el tipo más repetido (str)."""
    # TU CÓDIGO ACÁ
    pass


# Combinar tablas (merge)
# Combiná dos DataFrames por una columna en común. Pista: pd.merge(df1, df2, on=col).
# Ejemplo:  combinar(pokemon, tipos, "tipo")  →  una tabla con info de ambas
def combinar(df1, df2, col):
    """Devolvé el merge de df1 y df2 usando 'col' como clave."""
    # TU CÓDIGO ACÁ
    pass


# Tipos populares
# Cantidad de Pokémon por tipo, pero SOLO de los tipos que tienen 2 o más.
# Pista: contá por tipo y filtrá la Serie con [serie >= 2].
def tipos_populares(df):
    """Devolvé una Serie tipo → cantidad, solo con los tipos de 2+ Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Mínimo nivel por tipo
# Devolvé un dict tipo → nivel mínimo de ese tipo. Pista: df.groupby("tipo")["nivel"].min().
def minimo_por_tipo(df):
    """Devolvé un dict tipo → nivel mínimo."""
    # TU CÓDIGO ACÁ
    pass


# Suma de nivel por tipo
# Devolvé un dict tipo → suma de niveles de ese tipo.
def suma_nivel_por_tipo(df):
    """Devolvé un dict tipo → suma de niveles."""
    # TU CÓDIGO ACÁ
    pass


# Tipos distintos
# Devolvé una lista ORDENADA con los tipos distintos.
def tipos_distintos(df):
    """Devolvé los tipos distintos, ordenados."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de tipos
# Devolvé cuántos tipos DISTINTOS hay (como int).
def cantidad_tipos(df):
    """Devolvé cuántos tipos distintos hay."""
    # TU CÓDIGO ACÁ
    pass


# El tipo con más Pokémon
# Devolvé el tipo que tiene MÁS Pokémon. Pista: df.groupby("tipo").size().idxmax().
def tipo_con_mas_pokemon(df):
    """Devolvé el tipo con más Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Nombres por tipo
# Devolvé un dict tipo → lista de NOMBRES de ese tipo.
# Pista: df.groupby("tipo")["nombre"].apply(list).
def nombres_por_tipo(df):
    """Devolvé un dict tipo → lista de nombres."""
    # TU CÓDIGO ACÁ
    pass


# Nivel total
# Devolvé la suma de todos los niveles.
def nivel_total(df):
    """Devolvé la suma de los niveles."""
    # TU CÓDIGO ACÁ
    pass


# ¿Hay ese tipo?
# Devolvé True si hay al menos un Pokémon de tipo `tipo`.
def hay_tipo(df, tipo):
    """Devolvé True si existe ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Promedio de una columna
# Devolvé el promedio de la columna `col`.
def promedio_general(df, col):
    """Devolvé el promedio de la columna."""
    # TU CÓDIGO ACÁ
    pass


# Tipos ordenados por cantidad
# Devolvé los tipos ordenados de MÁS a menos Pokémon, como lista.
def ordenar_tipos_por_cantidad(df):
    """Devolvé los tipos ordenados por cantidad (desc)."""
    # TU CÓDIGO ACÁ
    pass


# El tipo con el nivel más alto
# Devolvé el tipo que tiene el Pokémon de mayor nivel.
# Pista: agrupá por tipo, tomá el máximo nivel de cada uno y quedate con el tipo del más alto.
def tipo_con_nivel_mas_alto(df):
    """Devolvé el tipo con el nivel más alto."""
    # TU CÓDIGO ACÁ
    pass


# Grupos grandes
# Devolvé una lista ORDENADA de los tipos que tienen al menos `minimo` Pokémon.
def filtrar_grupos_grandes(df, minimo):
    """Devolvé los tipos con al menos minimo Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Mediana de nivel por tipo
# Devolvé un dict tipo → mediana de los niveles de ese tipo. Pista: .median().
def mediana_por_tipo(df):
    """Devolvé un dict tipo → mediana de niveles."""
    # TU CÓDIGO ACÁ
    pass
