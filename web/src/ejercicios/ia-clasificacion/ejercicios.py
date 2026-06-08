"""✏️ Ejercicios — ML: clasificación

Clasificar = predecir una CATEGORÍA (ej: el tipo de un Pokémon por sus stats). Usamos
KNeighborsClassifier: mira los k vecinos más parecidos y vota. ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


# Entrenar el clasificador
# Entrená un clasificador KNN con k=3 vecinos y devolvé el modelo. Pista: KNeighborsClassifier(n_neighbors=3).fit(X, y).
def entrenar_clasificador(X, y):
    """Devolvé un KNN(3) entrenado con (X, y)."""
    # TU CÓDIGO ACÁ
    pass


# Clasificar uno
# Clasificá una fila y devolvé la categoría como int. Pista: int(modelo.predict([fila])[0]).
# Ejemplo:  clasificar(modelo, [89, 41])  →  0
def clasificar(modelo, fila):
    """Devolvé la categoría de 'fila' (int)."""
    # TU CÓDIGO ACÁ
    pass


# Clasificar varios
# Clasificá VARIAS filas de una y devolvé una lista de ints.
# Pista: [int(v) for v in modelo.predict(filas)].
# Ejemplo:  clasificar_varios(modelo, [[89, 41], [41, 89]])  →  [0, 1]
def clasificar_varios(modelo, filas):
    """Devolvé la lista de categorías (ints)."""
    # TU CÓDIGO ACÁ
    pass


# Precisión
# Devolvé la precisión del modelo sobre (X, y). Pista: modelo.score(X, y).
def precision(modelo, X, y):
    """Devolvé modelo.score(X, y)."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de clases
# Devolvé cuántas clases distintas hay en `y`.
def cantidad_clases(y):
    """Devolvé cuántas clases distintas hay."""
    # TU CÓDIGO ACÁ
    pass


# Contar por clase
# Devolvé un dict clase → cantidad.
def contar_por_clase(y):
    """Devolvé un dict clase → cantidad."""
    # TU CÓDIGO ACÁ
    pass


# Clase mayoritaria
# Devolvé la clase que más se repite (como int).
def clase_mayoritaria(y):
    """Devolvé la clase más frecuente."""
    # TU CÓDIGO ACÁ
    pass


# Etiquetas únicas
# Devolvé las clases distintas, ordenadas, como lista.
def etiquetas_unicas(y):
    """Devolvé las clases distintas, ordenadas."""
    # TU CÓDIGO ACÁ
    pass


# Accuracy
# Devolvé la fracción de aciertos entre predicciones y valores reales.
def accuracy(pred, real):
    """Devolvé la fracción de aciertos."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de aciertos
# Devolvé cuántas predicciones coinciden con el real (int).
def cantidad_aciertos(pred, real):
    """Devolvé cuántas coinciden."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de errores
# Devolvé cuántas predicciones NO coinciden (int).
def cantidad_errores(pred, real):
    """Devolvé cuántas no coinciden."""
    # TU CÓDIGO ACÁ
    pass


# Tasa de error
# Devolvé la fracción de errores (1 - accuracy).
def tasa_error(pred, real):
    """Devolvé la fracción de errores."""
    # TU CÓDIGO ACÁ
    pass


# ¿Todas correctas?
# Devolvé True si TODAS las predicciones coinciden con el real.
def todas_correctas(pred, real):
    """Devolvé True si todas coinciden."""
    # TU CÓDIGO ACÁ
    pass


# Índices incorrectos
# Devolvé los ÍNDICES donde la predicción NO coincide con el real, como lista.
# Ejemplo:  indices_incorrectos([1, 0, 1], [1, 1, 1])  →  [1]
def indices_incorrectos(pred, real):
    """Devolvé los índices de las predicciones erradas."""
    # TU CÓDIGO ACÁ
    pass


# ¿Es correcta la posición i?
# Devolvé True si la predicción en el índice `i` coincide con el real.
def es_correcta(pred, real, i):
    """Devolvé True si pred[i] == real[i]."""
    # TU CÓDIGO ACÁ
    pass


# Entrenar con k vecinos
# Creá un KNeighborsClassifier con n_neighbors=k, entrenalo con (X, y) y devolvelo.
def entrenar_con_vecinos(X, y, k):
    """Devolvé un KNN con k vecinos, ya entrenado."""
    # TU CÓDIGO ACÁ
    pass


# Predecir y contar
# Devolvé un dict clase → cantidad de las PREDICCIONES del modelo sobre X.
def predecir_y_contar(modelo, X):
    """Devolvé un dict clase → cantidad de las predicciones."""
    # TU CÓDIGO ACÁ
    pass


# Mayoría predicha
# Devolvé la clase que MÁS predijo el modelo sobre X (como int).
def mayoria_predicha(modelo, X):
    """Devolvé la clase más predicha."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de una clase
# Devolvé cuántas muestras de `y` son de la clase `clase` (int).
def cantidad_de_clase(y, clase):
    """Devolvé cuántas son de esa clase."""
    # TU CÓDIGO ACÁ
    pass


# ¿Hay esa clase?
# Devolvé True si la clase `clase` aparece en `y`.
def hay_clase(y, clase):
    """Devolvé True si aparece esa clase."""
    # TU CÓDIGO ACÁ
    pass
