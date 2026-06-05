# Líder Whitney — La Pokédex de Goldenrod (solución de referencia).
# El preamble (DATA) está en meta.json y se antepone al corregir.
import pandas as pd


def crear_pokedex(data):
    return pd.DataFrame(data)


def consultar_columna(df, col):
    return list(df[col])


def resumen_numerico(df, col):
    return {
        "minimo": int(df[col].min()),
        "maximo": int(df[col].max()),
        "promedio": round(float(df[col].mean()), 2),
    }


def ficha_pokemon(df, nombre):
    fila = df[df["nombre"] == nombre]
    if fila.empty:
        return "No encontrado."
    r = fila.iloc[0]
    return "%s | Tipo: %s | Nivel: %d | HP: %d" % (r["nombre"], r["tipo"], r["nivel"], r["hp"])
