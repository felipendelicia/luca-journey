"""✏️ Ejercicios — ML: evaluar modelos

Un modelo solo sirve si ACIERTA. Se separa en entrenamiento y prueba, y se mide la
EXACTITUD (accuracy) sobre datos que el modelo nunca vio. ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


# Exactitud (accuracy)
# Calculá la proporción de aciertos comparando lo real con lo predicho.
# Pista: accuracy_score(y_real, y_pred).
# Ejemplo:  precision([0, 1, 1, 0], [0, 1, 0, 0])  →  0.75   (3 de 4)
def precision(y_real, y_pred):
    """Devolvé accuracy_score(y_real, y_pred)."""
    # TU CÓDIGO ACÁ
    pass


# Entrenar y evaluar
# Dividí 50/50 (test_size=0.5, random_state=0), entrená un KNN(1) con el train y devolvé
# la exactitud sobre el test. Pista: accuracy_score(y_test, modelo.predict(X_test)).
def evaluar(X, y):
    """Devolvé la exactitud del KNN(1) sobre el test."""
    # TU CÓDIGO ACÁ
    pass


# El score del modelo
# Devolvé el score de un modelo YA entrenado sobre datos de prueba. Pista: modelo.score(X_test, y_test).
def score_modelo(modelo, X_test, y_test):
    """Devolvé modelo.score(X_test, y_test)."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de correctas
# Devolvé cuántas predicciones coinciden con el real (int).
def cantidad_correctas(y_real, y_pred):
    """Devolvé cuántas coinciden."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de errores
# Devolvé cuántas NO coinciden (int).
def cantidad_errores(y_real, y_pred):
    """Devolvé cuántas no coinciden."""
    # TU CÓDIGO ACÁ
    pass


# Tasa de error
# Devolvé la fracción de errores.
def tasa_error(y_real, y_pred):
    """Devolvé la fracción de errores."""
    # TU CÓDIGO ACÁ
    pass


# Verdaderos positivos
# Devolvé cuántos casos tienen real=1 Y predicción=1.
def verdaderos_positivos(y_real, y_pred):
    """Devolvé los verdaderos positivos."""
    # TU CÓDIGO ACÁ
    pass


# Falsos positivos
# Devolvé cuántos casos tienen real=0 PERO predicción=1.
def falsos_positivos(y_real, y_pred):
    """Devolvé los falsos positivos."""
    # TU CÓDIGO ACÁ
    pass


# Falsos negativos
# Devolvé cuántos casos tienen real=1 PERO predicción=0.
def falsos_negativos(y_real, y_pred):
    """Devolvé los falsos negativos."""
    # TU CÓDIGO ACÁ
    pass


# Verdaderos negativos
# Devolvé cuántos casos tienen real=0 Y predicción=0.
def verdaderos_negativos(y_real, y_pred):
    """Devolvé los verdaderos negativos."""
    # TU CÓDIGO ACÁ
    pass


# Precisión de la clase 1
# Devolvé verdaderos_positivos / (verdaderos_positivos + falsos_positivos).
def precision_clase1(y_real, y_pred):
    """Devolvé la precisión de la clase 1."""
    # TU CÓDIGO ACÁ
    pass


# Recall de la clase 1
# Devolvé verdaderos_positivos / (verdaderos_positivos + falsos_negativos).
def recall_clase1(y_real, y_pred):
    """Devolvé el recall de la clase 1."""
    # TU CÓDIGO ACÁ
    pass


# ¿Es perfecto?
# Devolvé True si TODAS las predicciones coinciden con el real.
def es_perfecto(y_real, y_pred):
    """Devolvé True si no hay errores."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de test
# Dado un total `n` y una fracción `frac` de test, devolvé cuántas muestras van a test:
# int(n * frac).
def cantidad_test(n, frac):
    """Devolvé cuántas muestras van a test."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de train
# Devolvé cuántas muestras van a entrenamiento: n - cantidad de test.
def cantidad_train(n, frac):
    """Devolvé cuántas muestras van a train."""
    # TU CÓDIGO ACÁ
    pass


# Promedio
# Devolvé el promedio de una lista de valores, como float.
def promedio(valores):
    """Devolvé el promedio."""
    # TU CÓDIGO ACÁ
    pass


# Entrenar KNN
# Creá un KNeighborsClassifier con n_neighbors=k, entrenalo con (X, y) y devolvelo.
def entrenar_knn(X, y, k):
    """Devolvé un KNN entrenado."""
    # TU CÓDIGO ACÁ
    pass


# Dividir datos
# Devolvé train_test_split(X, y, test_size=test_frac, random_state=seed) (4 partes).
def dividir_datos(X, y, test_frac, seed):
    """Devolvé X_train, X_test, y_train, y_test."""
    # TU CÓDIGO ACÁ
    pass


# Evaluar con split
# Partí (X, y) mitad y mitad (test_size=0.5, random_state=seed), entrená un KNN de 1 vecino
# con el train, y devolvé el accuracy_score sobre el test.
def evaluar_split(X, y, seed):
    """Devolvé el accuracy sobre el test."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de clases
# Devolvé cuántas clases distintas hay en `y`.
def cantidad_clases(y):
    """Devolvé cuántas clases distintas hay."""
    # TU CÓDIGO ACÁ
    pass
