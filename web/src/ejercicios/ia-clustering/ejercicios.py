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
