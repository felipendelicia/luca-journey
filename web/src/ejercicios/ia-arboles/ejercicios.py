"""✏️ Ejercicios — ML: árboles de decisión

Un árbol aprende reglas tipo "si ataque > 25 entonces Fuego". Es fácil de entender y
te dice qué tan IMPORTANTE fue cada feature para decidir. ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.tree import DecisionTreeClassifier


# Entrenar el árbol
# Entrená un árbol de decisión con random_state=0 (para que sea reproducible).
# Pista: DecisionTreeClassifier(random_state=0).fit(X, y).
def entrenar_arbol(X, y):
    """Devolvé un árbol entrenado."""
    # TU CÓDIGO ACÁ
    pass


# Clasificar con el árbol
# Clasificá una fila y devolvé un int. Pista: int(modelo.predict([fila])[0]).
def clasificar(modelo, fila):
    """Devolvé la categoría de 'fila' (int)."""
    # TU CÓDIGO ACÁ
    pass


# Importancia de las features
# Devolvé la importancia de cada feature como lista de floats. Pista: list(modelo.feature_importances_).
# Ejemplo:  si solo la 1ra feature decide  →  [1.0, 0.0]
def importancias(modelo):
    """Devolvé la lista de importancias."""
    # TU CÓDIGO ACÁ
    pass


# Precisión
# Devolvé modelo.score(X, y).
def precision(modelo, X, y):
    """Devolvé la precisión del modelo."""
    # TU CÓDIGO ACÁ
    pass


# Profundidad del árbol
# Devolvé la profundidad del árbol entrenado. Pista: modelo.get_depth().
def profundidad(modelo):
    """Devolvé la profundidad del árbol."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de hojas
# Devolvé cuántas hojas tiene el árbol. Pista: modelo.get_n_leaves().
def cantidad_hojas(modelo):
    """Devolvé la cantidad de hojas."""
    # TU CÓDIGO ACÁ
    pass


# Importancias como lista
# Devolvé las importancias de las features como lista. Pista: modelo.feature_importances_.tolist().
def importancias_lista(modelo):
    """Devolvé las importancias como lista."""
    # TU CÓDIGO ACÁ
    pass


# Feature más importante
# Devolvé el ÍNDICE de la feature más importante. Pista: np.argmax(modelo.feature_importances_).
def feature_mas_importante(modelo):
    """Devolvé el índice de la feature más importante."""
    # TU CÓDIGO ACÁ
    pass


# Entrenar con profundidad
# Creá un DecisionTreeClassifier con max_depth=prof y random_state=0, entrenalo con (X, y) y devolvelo.
def entrenar_con_profundidad(X, y, prof):
    """Devolvé un árbol con max_depth=prof, ya entrenado."""
    # TU CÓDIGO ACÁ
    pass


# Clasificar varios
# Devolvé las predicciones del modelo para una lista de filas, como lista.
def clasificar_varios(modelo, filas):
    """Devolvé las predicciones, como lista."""
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
# Devolvé la clase más frecuente (como int).
def clase_mayoritaria(y):
    """Devolvé la clase más frecuente."""
    # TU CÓDIGO ACÁ
    pass


# Accuracy
# Devolvé la fracción de aciertos entre predicciones y reales.
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


# Etiquetas únicas
# Devolvé las clases distintas, ordenadas, como lista.
def etiquetas_unicas(y):
    """Devolvé las clases distintas, ordenadas."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de features
# Devolvé cuántas columnas tiene X.
def cantidad_features(X):
    """Devolvé la cantidad de columnas de X."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de muestras
# Devolvé cuántas filas tiene X.
def cantidad_muestras(X):
    """Devolvé la cantidad de filas de X."""
    # TU CÓDIGO ACÁ
    pass


# Predecir y contar
# Devolvé un dict clase → cantidad de las PREDICCIONES del modelo sobre X.
def predecir_y_contar(modelo, X):
    """Devolvé un dict clase → cantidad de predicciones."""
    # TU CÓDIGO ACÁ
    pass


# ¿Hay esa clase?
# Devolvé True si la clase `clase` aparece en `y`.
def hay_clase(y, clase):
    """Devolvé True si aparece esa clase."""
    # TU CÓDIGO ACÁ
    pass
