"""✅ Soluciones — pandas: Limpieza de datos"""
import pandas as pd


def contar_nulos(df):
    return int(df.isna().sum().sum())


def rellenar_ceros(df, col):
    nuevo = df.copy()
    nuevo[col] = nuevo[col].fillna(0)
    return nuevo


def quitar_filas_nulas(df):
    return df.dropna()


def a_entero(serie):
    return serie.astype(int)


def sin_duplicados(df):
    return df.drop_duplicates()


def renombrar(df, viejo, nuevo):
    return df.rename(columns={viejo: nuevo})


def a_mayusculas(serie):
    return serie.str.upper()


def aplicar(serie, funcion):
    return serie.apply(funcion)
