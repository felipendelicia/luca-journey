"""✏️ Ejercicios — ML: tu primer modelo

Machine Learning = enseñarle a un modelo con EJEMPLOS para que después prediga solo.
Le das X (datos) e y (respuestas), hace .fit() y después .predict(). Usamos un
clasificador de vecinos (KNN). ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


# Crear el modelo (KNN)
# Devolvé un clasificador KNN que mire al vecino más cercano. Pista: KNeighborsClassifier(n_neighbors=1).
def crear_modelo():
    """Devolvé un KNeighborsClassifier(n_neighbors=1)."""
    # TU CÓDIGO ACÁ
    pass


# Entrenar (fit)
# Entrená el modelo con los datos X y las etiquetas y, y devolvé el modelo entrenado.
# Pista: modelo.fit(X, y); return modelo.
def entrenar(modelo, X, y):
    """Entrená el modelo y devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Predecir (predict)
# Predecí la etiqueta de UNA fila y devolvé un int. Pista: int(modelo.predict([fila])[0]).
# Ejemplo:  para stats de Fuego  →  predecir(modelo, [88, 42])  →  0
def predecir(modelo, fila):
    """Devolvé la predicción de 'fila' como int."""
    # TU CÓDIGO ACÁ
    pass


# Todo junto
# Creá un KNN(1), entrenalo con (X, y) y predecí 'fila'. Devolvé un int.
def entrenar_y_predecir(X, y, fila):
    """Combiná crear + entrenar + predecir."""
    # TU CÓDIGO ACÁ
    pass


# Predecir varios
# Devolvé las predicciones del modelo para una lista de filas, como lista. Pista: modelo.predict(filas).tolist().
def predecir_varios(modelo, filas):
    """Devolvé las predicciones para varias filas, como lista."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de clases
# Devolvé cuántas clases DISTINTAS hay en `y`. Pista: np.unique.
def cantidad_clases(y):
    """Devolvé cuántas clases distintas hay."""
    # TU CÓDIGO ACÁ
    pass


# Precisión
# Devolvé la precisión del modelo sobre (X, y). Pista: modelo.score(X, y).
def precision(modelo, X, y):
    """Devolvé modelo.score(X, y)."""
    # TU CÓDIGO ACÁ
    pass


# Contar por clase
# Devolvé un dict clase → cantidad. Pista: np.unique(y, return_counts=True).
# Ejemplo:  contar_por_clase(np.array([0, 0, 1]))  →  {0: 2, 1: 1}
def contar_por_clase(y):
    """Devolvé un dict clase → cantidad."""
    # TU CÓDIGO ACÁ
    pass


# Clase mayoritaria
# Devolvé la clase que más se repite en `y` (como int).
def clase_mayoritaria(y):
    """Devolvé la clase más frecuente."""
    # TU CÓDIGO ACÁ
    pass


# Accuracy manual
# Recibís predicciones y valores reales. Devolvé la FRACCIÓN de aciertos (float).
# Ejemplo:  accuracy_manual([1, 0, 1], [1, 1, 1])  →  0.666...
def accuracy_manual(pred, real):
    """Devolvé la fracción de aciertos."""
    # TU CÓDIGO ACÁ
    pass


# Etiquetas únicas
# Devolvé las clases distintas, ordenadas, como lista. Pista: np.unique(y).tolist().
def etiquetas_unicas(y):
    """Devolvé las clases distintas, ordenadas."""
    # TU CÓDIGO ACÁ
    pass


# Promedio por columna
# Devolvé el promedio de cada columna de X (usá axis=0).
def promedio_por_columna(X):
    """Devolvé el promedio de cada columna."""
    # TU CÓDIGO ACÁ
    pass


# Escalar a 0..1
# Devolvé X escalado por columna al rango 0..1: (X - mínimo) / (máximo - mínimo).
# Pista: X.min(axis=0) y X.max(axis=0).
def escalar_0_1(X):
    """Devolvé X escalado a 0..1 por columna."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de features
# Devolvé cuántas columnas (características) tiene X. Pista: X.shape[1].
def cantidad_features(X):
    """Devolvé la cantidad de columnas de X."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de muestras
# Devolvé cuántas filas (muestras) tiene X. Pista: X.shape[0].
def cantidad_muestras(X):
    """Devolvé la cantidad de filas de X."""
    # TU CÓDIGO ACÁ
    pass


# Distancia euclídea
# Devolvé la distancia euclídea entre dos puntos `a` y `b`.
# Ejemplo:  distancia_euclidea([0, 0], [3, 4])  →  5.0
def distancia_euclidea(a, b):
    """Devolvé la distancia entre a y b."""
    # TU CÓDIGO ACÁ
    pass


# Índice del más cercano
# Devolvé el ÍNDICE del punto de `puntos` más cercano a `punto`.
# Ejemplo:  indice_mas_cercano([0, 0], [[10, 10], [1, 1]])  →  1
def indice_mas_cercano(punto, puntos):
    """Devolvé el índice del punto más cercano."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de aciertos
# Recibís predicciones y reales. Devolvé CUÁNTAS coinciden (int).
def cantidad_correctas(pred, real):
    """Devolvé cuántas predicciones coinciden."""
    # TU CÓDIGO ACÁ
    pass


# Matriz a lista
# Devolvé X (un array de NumPy) convertido a lista de listas. Pista: X.tolist().
def matriz_a_lista(X):
    """Devolvé X como lista de listas."""
    # TU CÓDIGO ACÁ
    pass


# Entrenar con k vecinos
# Creá un KNeighborsClassifier con n_neighbors=k, entrenalo con (X, y) y devolvelo.
def entrenar_con_k(X, y, k):
    """Devolvé un KNN con k vecinos, ya entrenado."""
    # TU CÓDIGO ACÁ
    pass
