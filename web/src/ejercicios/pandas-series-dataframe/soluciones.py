"""✅ Soluciones — pandas: Series y DataFrame"""
import pandas as pd


def crear_serie(valores):
    return pd.Series(valores)


def serie_con_indices(valores, nombres):
    return pd.Series(valores, index=nombres)


def crear_pokedex(datos):
    return pd.DataFrame(datos)


def nombres_columnas(df):
    return list(df.columns)


def columna(df, nombre):
    return df[nombre]


def cantidad_filas(df):
    return len(df)


def primeras_filas(df, n):
    return df.head(n)


def promedio_columna(df, col):
    return df[col].mean()


def agregar_columna(df, nombre, valores):
    nuevo = df.copy()
    nuevo[nombre] = valores
    return nuevo


def suma_columna(df, col):
    return df[col].sum()


def maximo_columna(df, col):
    return df[col].max()


def minimo_columna(df, col):
    return df[col].min()


def columna_a_lista(df, col):
    return df[col].tolist()


def cantidad_columnas(df):
    return len(df.columns)


def existe_columna(df, col):
    return col in df.columns


def contar_donde(df, col, n):
    return int((df[col] > n).sum())


def valores_ordenados(df, col):
    return df.sort_values(col)[col].tolist()


def fila_como_dict(df, i):
    return df.iloc[i].to_dict()


def renombrar_columnas(df, mapa):
    return list(df.rename(columns=mapa).columns)


def mediana_columna(df, col):
    return df[col].median()
