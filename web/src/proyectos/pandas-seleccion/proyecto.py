# Líder Morty — El registro de Ecruteak (solución de referencia).
# El preamble (REGISTRO) está en meta.json y se antepone al corregir.
import pandas as pd


def filtrar_nivel_minimo(df, minimo):
    return df[df["nivel"] >= minimo]


def de_tipo(df, tipo):
    return df[df["tipo"] == tipo]


def top_n(df, n):
    ordenado = df.sort_values("nivel", ascending=False)
    return list(ordenado["nombre"].head(n))


def buscar_y_mostrar(df, tipo, nivel_minimo):
    filtrado = de_tipo(df, tipo)
    filtrado = filtrar_nivel_minimo(filtrado, nivel_minimo)
    ordenado = filtrado.sort_values("nivel", ascending=False)
    return ["%s (Lv.%d)" % (row["nombre"], row["nivel"]) for _, row in ordenado.iterrows()]
