# Líder Pryce — El gráfico del Hielo (solución de referencia).
# El preamble (EQUIPO) está en meta.json y se antepone al corregir.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


def datos_barras(df):
    return list(df["nombre"]), list(df["nivel"])


def datos_dispersion(df):
    return list(df["nivel"]), list(df["hp"])


def datos_histograma(df, col):
    return list(df[col])


def graficar_equipo(df):
    nombres, niveles = datos_barras(df)
    fig, ax = plt.subplots()
    ax.bar(nombres, niveles)
    ax.set_title("Niveles del equipo de Pryce")
    plt.close(fig)
    return nombres, niveles
