"""✅ Soluciones — Análisis integrador"""
import pandas as pd


def cargar(datos):
    return pd.DataFrame(datos)


def limpiar(df):
    return df.dropna().reset_index(drop=True)


def cantidad(df):
    return len(df)


def tipo_mas_comun(df):
    return df["tipo"].value_counts().idxmax()


def nivel_promedio(df):
    return df["nivel"].mean()


def top_n(df, n):
    return df.sort_values("nivel", ascending=False).head(n)


def promedio_por_tipo(df):
    return df.groupby("tipo")["nivel"].mean()


def campeon_del_tipo(df, tipo):
    deltipo = df[df["tipo"] == tipo]
    return deltipo.loc[deltipo["nivel"].idxmax(), "nombre"]
