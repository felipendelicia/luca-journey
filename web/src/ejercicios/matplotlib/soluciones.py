"""✅ Soluciones — matplotlib: Gráficos"""


def dibujar_barras(ax, nombres, valores):
    ax.bar(nombres, valores)
    return ax


def poner_titulo(ax, titulo):
    ax.set_title(titulo)
    return ax


def poner_etiquetas(ax, etiqueta_x, etiqueta_y):
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    return ax


def dibujar_linea(ax, x, y):
    ax.plot(x, y)
    return ax


def dibujar_dispersion(ax, x, y):
    ax.scatter(x, y)
    return ax


def dibujar_histograma(ax, datos):
    ax.hist(datos)
    return ax
