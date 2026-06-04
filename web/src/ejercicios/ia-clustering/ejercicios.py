"""
✏️ Ejercicios — ML: clustering (no supervisado)

Hasta ahora teníamos las respuestas (y). En el aprendizaje NO supervisado, el modelo
agrupa solo los datos parecidos, sin que le digamos las categorías. Usamos KMeans.
"""
import numpy as np
from sklearn.cluster import KMeans


# 1) Agrupá los datos en k grupos. Usá random_state=0 y n_init=10. Devolvé el modelo.
def agrupar(X, k):
    """KMeans(n_clusters=k, random_state=0, n_init=10).fit(X)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Devolvé a qué grupo quedó asignado cada dato (una lista de ints).
def etiquetas(modelo):
    """Pista: [int(e) for e in modelo.labels_]."""
    # TU CÓDIGO ACÁ
    pass


# 3) ¿A qué grupo pertenece una fila nueva? Devolvé un int.
def a_que_grupo(modelo, fila):
    """int(modelo.predict([fila])[0])."""
    # TU CÓDIGO ACÁ
    pass
