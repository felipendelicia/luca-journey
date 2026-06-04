"""✅ Soluciones — pandas: Selección y filtrado"""
import pandas as pd


def fila_por_posicion(df, i):
    return df.iloc[i]


def filtrar_nivel(df, minimo):
    return df[df["nivel"] >= minimo]


def de_tipo(df, tipo):
    return df[df["tipo"] == tipo]


def ordenar_por_nivel(df):
    return df.sort_values("nivel", ascending=False)


def nombres_fuertes(df, minimo):
    return list(df[df["nivel"] >= minimo]["nombre"])


def solo_columnas(df, cols):
    return df[cols]


def quitar_columna(df, col):
    return df.drop(columns=[col])


def el_mas_fuerte(df):
    return df.loc[df["nivel"].idxmax(), "nombre"]
