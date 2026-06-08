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


def minimo_por_tipo(df):
    return df.groupby("tipo")["nivel"].min().to_dict()


def suma_nivel_por_tipo(df):
    return df.groupby("tipo")["nivel"].sum().to_dict()


def tipos_distintos(df):
    return sorted(df["tipo"].unique().tolist())


def cantidad_tipos(df):
    return int(df["tipo"].nunique())


def tipo_con_mas_pokemon(df):
    return df.groupby("tipo").size().idxmax()


def nombres_por_tipo(df):
    return df.groupby("tipo")["nombre"].apply(list).to_dict()


def nivel_total(df):
    return df["nivel"].sum()


def hay_tipo(df, tipo):
    return tipo in df["tipo"].values


def promedio_general(df, col):
    return df[col].mean()


def ordenar_tipos_por_cantidad(df):
    return df.groupby("tipo").size().sort_values(ascending=False).index.tolist()


def tipo_con_nivel_mas_alto(df):
    return df.groupby("tipo")["nivel"].max().idxmax()


def filtrar_grupos_grandes(df, minimo):
    conteos = df.groupby("tipo").size()
    return sorted(conteos[conteos >= minimo].index.tolist())


def mediana_por_tipo(df):
    return df.groupby("tipo")["nivel"].median().to_dict()
