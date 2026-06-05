# Líder Clair — El análisis del Dragón (solución de referencia).
# El preamble (DRAGONES) está en meta.json y se antepone al corregir.
import pandas as pd


def filtrar_elite(df, nivel_minimo):
    return df[df["nivel"] >= nivel_minimo].sort_values("nivel", ascending=False)


def resumen_por_tipo(df):
    resultado = {}
    for tipo, grupo in df.groupby("tipo"):
        resultado[tipo] = {
            "cantidad": int(len(grupo)),
            "nivel_promedio": round(float(grupo["nivel"].mean()), 1),
            "victorias_totales": int(grupo["victorias"].sum()),
        }
    return resultado


def mvp(df):
    return df.loc[df["victorias"].idxmax(), "nombre"]


def reporte_final(df):
    elite = list(filtrar_elite(df, 35)["nombre"])
    mv = mvp(df)
    victorias_por_tipo = df.groupby("tipo")["victorias"].sum()
    tipo_dom = victorias_por_tipo.idxmax()
    victoria_rate = round(float(df["victorias"].sum()) / len(df), 2)
    return {
        "elite": elite,
        "mvp": mv,
        "tipo_dominante": tipo_dom,
        "victoria_rate": victoria_rate,
    }
