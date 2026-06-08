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


def mediana_nivel(df):
    return df["nivel"].median()


def proporcion_tipo(df, tipo):
    return float((df["tipo"] == tipo).mean())


def nombres_top(df, n):
    return df.sort_values("nivel", ascending=False).head(n)["nombre"].tolist()


def tipos_unicos(df):
    return sorted(df["tipo"].unique().tolist())


def filtrar_fuertes(df, minimo):
    return df[df["nivel"] >= minimo]["nombre"].tolist()


def rango_niveles(df):
    return int(df["nivel"].max() - df["nivel"].min())


def tipo_con_mayor_promedio(df):
    return df.groupby("tipo")["nivel"].mean().idxmax()


def contar_por_rango(df, lo, hi):
    return int(((df["nivel"] >= lo) & (df["nivel"] <= hi)).sum())


def nivel_total(df):
    return df["nivel"].sum()


def hay_fuertes(df, umbral):
    return bool((df["nivel"] >= umbral).any())


def tabla_resumen(df):
    return {"total": len(df), "tipos": int(df["tipo"].nunique()), "nivel_total": int(df["nivel"].sum())}


def cantidad_por_tipo(df):
    return df.groupby("tipo").size().to_dict()
