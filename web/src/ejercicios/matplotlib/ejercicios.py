"""✏️ Ejercicios — matplotlib: Gráficos

Cada función recibe un 'ax' (un eje de matplotlib, ya creado). Dibujá o configurá
algo sobre él y devolvé el mismo ax al final. ✅ Corregir al terminar.
"""


# Gráfico de barras
# Dibujá un gráfico de barras con nombres (eje x) y valores (alturas). Pista: ax.bar(nombres, valores).
# Acordate de devolver ax al final.
def dibujar_barras(ax, nombres, valores):
    """Dibujá las barras y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Poner un título
# Ponele un título al gráfico. Pista: ax.set_title(titulo). Devolvé ax.
def poner_titulo(ax, titulo):
    """Poné el título y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Etiquetas de los ejes
# Ponele nombre al eje X y al eje Y. Pista: ax.set_xlabel(...) y ax.set_ylabel(...). Devolvé ax.
def poner_etiquetas(ax, etiqueta_x, etiqueta_y):
    """Poné las etiquetas de los ejes y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Gráfico de línea
# Dibujá una línea que una los puntos (x, y). Pista: ax.plot(x, y). Devolvé ax.
def dibujar_linea(ax, x, y):
    """Dibujá la línea y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Gráfico de dispersión
# Dibujá puntos sueltos en las posiciones (x, y). Pista: ax.scatter(x, y). Devolvé ax.
def dibujar_dispersion(ax, x, y):
    """Dibujá los puntos y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Histograma
# Dibujá un histograma a partir de una lista de datos. Pista: ax.hist(datos). Devolvé ax.
def dibujar_histograma(ax, datos):
    """Dibujá el histograma y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Límites del eje X
# Poné el rango del eje X entre `lo` y `hi`. Pista: ax.set_xlim(lo, hi). Devolvé ax.
def poner_limites_x(ax, lo, hi):
    """Fijá los límites del eje X y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Límites del eje Y
# Poné el rango del eje Y entre `lo` y `hi`. Pista: ax.set_ylim(lo, hi). Devolvé ax.
def poner_limites_y(ax, lo, hi):
    """Fijá los límites del eje Y y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Barras horizontales
# Dibujá barras HORIZONTALES con nombres y valores. Pista: ax.barh(nombres, valores). Devolvé ax.
def dibujar_barras_horizontales(ax, nombres, valores):
    """Dibujá barras horizontales y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Gráfico de torta
# Dibujá una torta con los `valores`. Pista: ax.pie(valores). Devolvé ax.
def dibujar_torta(ax, valores):
    """Dibujá la torta y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Dos líneas
# Dibujá dos líneas sobre el mismo eje: (x, y1) y (x, y2). Devolvé ax.
def dibujar_dos_lineas(ax, x, y1, y2):
    """Dibujá las dos líneas y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Cuántas líneas
# Devolvé cuántas líneas tiene el gráfico. Pista: len(ax.lines).
def cantidad_lineas(ax):
    """Devolvé la cantidad de líneas dibujadas."""
    # TU CÓDIGO ACÁ
    pass


# Cuántas barras
# Devolvé cuántas barras tiene el gráfico. Pista: len(ax.patches).
def cantidad_barras(ax):
    """Devolvé la cantidad de barras dibujadas."""
    # TU CÓDIGO ACÁ
    pass


# Título actual
# Devolvé el título actual del gráfico. Pista: ax.get_title().
def titulo_actual(ax):
    """Devolvé el título del gráfico."""
    # TU CÓDIGO ACÁ
    pass


# Etiqueta X actual
# Devolvé la etiqueta actual del eje X. Pista: ax.get_xlabel().
def etiqueta_x_actual(ax):
    """Devolvé la etiqueta del eje X."""
    # TU CÓDIGO ACÁ
    pass


# Limpiar
# Borrá todo lo dibujado en el eje. Pista: ax.cla(). Devolvé ax.
def limpiar(ax):
    """Limpiá el eje y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Título y etiquetas de una
# Poné el título, la etiqueta X y la etiqueta Y. Devolvé ax.
def poner_titulo_y_etiquetas(ax, titulo, ex, ey):
    """Poné título y etiquetas, devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Agregar un punto
# Dibujá un único punto (x, y) en el gráfico. Pista: ax.scatter([x], [y]). Devolvé ax.
def agregar_punto(ax, x, y):
    """Dibujá el punto y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Invertir el eje Y
# Dá vuelta el eje Y (de mayor a menor). Pista: ax.invert_yaxis(). Devolvé ax.
def invertir_eje_y(ax):
    """Invertí el eje Y y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass


# Línea horizontal
# Dibujá una línea horizontal a la altura `y`. Pista: ax.axhline(y). Devolvé ax.
def marcar_horizontal(ax, y):
    """Dibujá una línea horizontal y devolvé ax."""
    # TU CÓDIGO ACÁ
    pass
