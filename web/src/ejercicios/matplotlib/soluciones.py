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


def poner_limites_x(ax, lo, hi):
    ax.set_xlim(lo, hi)
    return ax


def poner_limites_y(ax, lo, hi):
    ax.set_ylim(lo, hi)
    return ax


def dibujar_barras_horizontales(ax, nombres, valores):
    ax.barh(nombres, valores)
    return ax


def dibujar_torta(ax, valores):
    ax.pie(valores)
    return ax


def dibujar_dos_lineas(ax, x, y1, y2):
    ax.plot(x, y1)
    ax.plot(x, y2)
    return ax


def cantidad_lineas(ax):
    return len(ax.lines)


def cantidad_barras(ax):
    return len(ax.patches)


def titulo_actual(ax):
    return ax.get_title()


def etiqueta_x_actual(ax):
    return ax.get_xlabel()


def limpiar(ax):
    ax.cla()
    return ax


def poner_titulo_y_etiquetas(ax, titulo, ex, ey):
    ax.set_title(titulo)
    ax.set_xlabel(ex)
    ax.set_ylabel(ey)
    return ax


def agregar_punto(ax, x, y):
    ax.scatter([x], [y])
    return ax


def invertir_eje_y(ax):
    ax.invert_yaxis()
    return ax


def marcar_horizontal(ax, y):
    ax.axhline(y)
    return ax
