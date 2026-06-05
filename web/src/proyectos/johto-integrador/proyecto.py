# Liga de Johto — Integrador (solución de referencia).
# El preamble (LIGA) está en meta.json y se antepone al corregir.
import numpy as np
import pandas as pd


def preparar_stats(df):
    return np.column_stack([df["hp"].values, df["ataque"].values])


def normalizar_columna(df, col):
    arr = df[col].values.astype(float)
    return (arr - arr.min()) / (arr.max() - arr.min())


def ranking_por_tipo(df):
    agrupado = df.groupby("tipo").agg(
        cantidad=("nombre", "count"),
        nivel_max=("nivel", "max"),
        victorias_totales=("victorias", "sum"),
    ).reset_index()
    return agrupado.sort_values("victorias_totales", ascending=False).reset_index(drop=True)


def informe_liga(df):
    return {
        "total_pokemon": len(df),
        "nivel_promedio": round(float(df["nivel"].mean()), 2),
        "mvp": df.loc[df["victorias"].idxmax(), "nombre"],
        "tipo_dominante": df.groupby("tipo")["victorias"].sum().idxmax(),
        "stats_normalizadas": normalizar_columna(df, "nivel"),
    }


def reporte_texto(df):
    info = informe_liga(df)
    return (
        "Liga de Johto — Informe\n"
        "Total: %d Pokémon\n"
        "Nivel promedio: %s\n"
        "MVP: %s\n"
        "Tipo dominante: %s"
    ) % (info["total_pokemon"], info["nivel_promedio"], info["mvp"], info["tipo_dominante"])
