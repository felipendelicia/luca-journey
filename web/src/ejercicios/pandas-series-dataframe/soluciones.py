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
