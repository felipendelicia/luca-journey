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


def nombres(df):
    return df["nombre"].tolist()


def valor_en(df, fila, col):
    return df.iloc[fila][col]


def ultima_fila(df):
    return df.iloc[-1].to_dict()


def mas_debil(df):
    return df.loc[df["nivel"].idxmin()].to_dict()


def nivel_de(df, nombre):
    filtrado = df[df["nombre"] == nombre]
    if len(filtrado) == 0:
        return None
    return filtrado.iloc[0]["nivel"]


def existe_nombre(df, nombre):
    return nombre in df["nombre"].values


def primeros_nombres(df, n):
    return df["nombre"].head(n).tolist()


def ordenar_nombres(df):
    return sorted(df["nombre"].tolist())


def contar_tipo(df, tipo):
    return int((df["tipo"] == tipo).sum())


def niveles_entre(df, lo, hi):
    return df[(df["nivel"] >= lo) & (df["nivel"] <= hi)]["nombre"].tolist()


def top_niveles(df, n):
    return df["nivel"].sort_values(ascending=False).head(n).tolist()


def nombres_de_tipo(df, tipo):
    return df[df["tipo"] == tipo]["nombre"].tolist()
