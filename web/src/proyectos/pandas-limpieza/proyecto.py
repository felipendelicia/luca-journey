# Líder Chuck — El censo de Cianwood (solución de referencia).
# El preamble (CENSO) está en meta.json y se antepone al corregir.
import pandas as pd


def contar_nulos(df):
    return int(df.isna().sum().sum())


def limpiar_tipos(df):
    df = df.copy()
    df["nivel"] = df["nivel"].fillna(0).astype(int)
    df["tipo"] = df["tipo"].fillna("Desconocido")
    return df


def sin_duplicados(df):
    return df.drop_duplicates()


def censo_limpio(df):
    df = sin_duplicados(df)
    df = limpiar_tipos(df)
    df = df.dropna(subset=["hp"])
    return df
