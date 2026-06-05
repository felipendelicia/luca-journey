# Líder Skyla — Árbol de decisión (solución de referencia).
# El preamble (X_ARBOL, Y_ARBOL) está en meta.json y se antepone al corregir.

from sklearn.tree import DecisionTreeClassifier


def entrenar_arbol(X, y):
    return DecisionTreeClassifier(random_state=0).fit(X, y)


def clasificar_arbol(arbol, fila):
    return int(arbol.predict([fila])[0])


def importancias(arbol):
    return list(arbol.feature_importances_)


def analizar_equipo(equipo):
    arbol = entrenar_arbol(X_ARBOL, Y_ARBOL)
    predicciones = [clasificar_arbol(arbol, fila) for fila in equipo]
    return {
        "puede_evolucionar": predicciones.count(1),
        "no_puede": predicciones.count(0),
    }
