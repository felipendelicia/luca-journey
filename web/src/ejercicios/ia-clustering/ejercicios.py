"""✏️ Ejercicios — ML: clustering (no supervisado)

Hasta ahora teníamos las respuestas (y). En el aprendizaje NO supervisado, el modelo
agrupa solo los datos parecidos, sin etiquetas. Usamos KMeans. ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.cluster import KMeans


# Agrupar (KMeans)
# Agrupá los datos en k grupos. Usá random_state=0 y n_init=10. Devolvé el modelo.
# Pista: KMeans(n_clusters=k, random_state=0, n_init=10).fit(X).
def agrupar(X, k):
    """Devolvé un KMeans entrenado con k grupos."""
    # TU CÓDIGO ACÁ
    pass


# A qué grupo fue cada uno
# Devolvé a qué grupo quedó asignado cada dato, como lista de ints.
# Pista: [int(e) for e in modelo.labels_].
def etiquetas(modelo):
    """Devolvé la lista de grupos de cada dato."""
    # TU CÓDIGO ACÁ
    pass


# Grupo de uno nuevo
# ¿A qué grupo pertenece una fila nueva? Devolvé un int. Pista: int(modelo.predict([fila])[0]).
def a_que_grupo(modelo, fila):
    """Devolvé el grupo de 'fila' (int)."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de grupos
# Devolvé cuántos grupos tiene el modelo. Pista: modelo.n_clusters.
def cantidad_grupos(modelo):
    """Devolvé la cantidad de grupos."""
    # TU CÓDIGO ACÁ
    pass


# A qué grupos
# Devolvé el grupo asignado a cada fila de `filas`, como lista. Pista: modelo.predict(filas).tolist().
def a_que_grupos(modelo, filas):
    """Devolvé el grupo de cada fila, como lista."""
    # TU CÓDIGO ACÁ
    pass


# Tamaño de cada grupo
# Devolvé un dict grupo → cantidad de puntos, usando las etiquetas del modelo (modelo.labels_).
def tamano_grupos(modelo):
    """Devolvé un dict grupo → cantidad de puntos."""
    # TU CÓDIGO ACÁ
    pass


# ¿Mismo grupo?
# Devolvé True si `fila1` y `fila2` caen en el mismo grupo.
def mismo_grupo(modelo, fila1, fila2):
    """Devolvé True si las dos filas caen en el mismo grupo."""
    # TU CÓDIGO ACÁ
    pass


# Agrupar con k grupos
# Creá un KMeans con n_clusters=k, random_state=0 y n_init=10, entrenalo con X y devolvelo.
def agrupar_con_k(X, k):
    """Devolvé un KMeans con k grupos, ya entrenado."""
    # TU CÓDIGO ACÁ
    pass


# Distancia euclídea
# Devolvé la distancia euclídea entre dos puntos `a` y `b`.
def distancia_euclidea(a, b):
    """Devolvé la distancia entre a y b."""
    # TU CÓDIGO ACÁ
    pass


# Índice del más cercano
# Devolvé el ÍNDICE del punto de `puntos` más cercano a `punto`.
def indice_mas_cercano(punto, puntos):
    """Devolvé el índice del punto más cercano."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad por etiqueta
# Recibís una lista/array de etiquetas. Devolvé un dict etiqueta → cantidad.
def cantidad_por_etiqueta(etiquetas):
    """Devolvé un dict etiqueta → cantidad."""
    # TU CÓDIGO ACÁ
    pass


# Grupos distintos
# Devolvé las etiquetas distintas, ordenadas, como lista.
def grupos_distintos(etiquetas):
    """Devolvé las etiquetas distintas, ordenadas."""
    # TU CÓDIGO ACÁ
    pass


# Grupo mayoritario
# Devolvé la etiqueta que más se repite (como int).
def grupo_mayoritario(etiquetas):
    """Devolvé la etiqueta más frecuente."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de puntos en un grupo
# Devolvé cuántas etiquetas son iguales a `grupo` (int).
def cantidad_puntos_en(etiquetas, grupo):
    """Devolvé cuántos puntos hay en ese grupo."""
    # TU CÓDIGO ACÁ
    pass


# Promedio de un grupo
# Devolvé el promedio (por columna) de las filas de X cuyo grupo (en `etiquetas`) sea `grupo`.
# Ejemplo:  X=[[2,2],[4,4],[100,100]], etiquetas=[0,0,1], grupo=0  →  [3.0, 3.0]
def promedio_de_grupo(X, etiquetas, grupo):
    """Devolvé el promedio de las filas de ese grupo."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de muestras
# Devolvé cuántas filas tiene X.
def cantidad_muestras(X):
    """Devolvé la cantidad de filas de X."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de features
# Devolvé cuántas columnas tiene X.
def cantidad_features(X):
    """Devolvé la cantidad de columnas de X."""
    # TU CÓDIGO ACÁ
    pass


# Grupo de un punto
# Devolvé el grupo al que el modelo asigna `punto` (como int).
def centro_mas_cercano(modelo, punto):
    """Devolvé el grupo de ese punto."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de grupos usados
# Devolvé cuántos grupos DISTINTOS aparecen en `etiquetas`.
def cantidad_grupos_usados(etiquetas):
    """Devolvé cuántos grupos distintos hay."""
    # TU CÓDIGO ACÁ
    pass


# ¿Inercia positiva?
# Devolvé True si la inercia del modelo es mayor que 0. Pista: modelo.inertia_.
def inercia_positiva(modelo):
    """Devolvé True si la inercia es > 0."""
    # TU CÓDIGO ACÁ
    pass
