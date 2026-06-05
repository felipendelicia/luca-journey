# Líder Jasmine — El ranking del Acero (solución de referencia).
# El preamble (RANKING) está en meta.json y se antepone al corregir.
import pandas as pd


def contar_por_tipo(df):
    return dict(df["tipo"].value_counts())


def nivel_promedio_por_tipo(df):
    serie = df.groupby("tipo")["nivel"].mean()
    return {tipo: round(float(v), 2) for tipo, v in serie.items()}


def tipo_mas_victorias(df):
    return df.groupby("tipo")["victorias"].sum().idxmax()


def resumen_por_tipo(df):
    conteo = df.groupby("tipo").agg(
        cantidad=("nombre", "count"),
        nivel_prom=("nivel", "mean"),
        victorias=("victorias", "sum"),
    ).sort_index()
    resultado = []
    for tipo, row in conteo.iterrows():
        resultado.append(
            "%s: %d Pokémon | Nivel promedio: %.1f | Victorias: %d"
            % (tipo, row["cantidad"], row["nivel_prom"], row["victorias"])
        )
    return resultado
