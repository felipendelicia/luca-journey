"""✅ Soluciones — pandas: Agrupar y combinar"""
import pandas as pd


def contar_por_tipo(df):
    return df["tipo"].value_counts()


def nivel_promedio_por_tipo(df):
    return df.groupby("tipo")["nivel"].mean()


def nivel_maximo_por_tipo(df):
    return df.groupby("tipo")["nivel"].max()


def hp_total_por_tipo(df):
    return df.groupby("tipo")["hp"].sum()


def tipo_mas_comun(df):
    return df["tipo"].value_counts().idxmax()


def combinar(df1, df2, col):
    return pd.merge(df1, df2, on=col)


def tipos_populares(df):
    conteo = df["tipo"].value_counts()
    return conteo[conteo >= 2]
