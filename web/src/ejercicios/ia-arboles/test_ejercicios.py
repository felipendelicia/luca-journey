"""🧪 Tests — ML: árboles de decisión"""
import importlib.util
import os

import numpy as np
from sklearn.tree import DecisionTreeClassifier

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"iaarb_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))

# la decisión depende SOLO de la 1ra columna (ataque); la 2da es constante
X = np.array([[10, 5], [20, 5], [30, 5], [40, 5]])
y = np.array([0, 0, 1, 1])


def test_entrenar_arbol():
    m = modulo.entrenar_arbol(X, y)
    assert isinstance(m, DecisionTreeClassifier)
    assert m.predict([[15, 5]])[0] == 0
    assert m.predict([[35, 5]])[0] == 1


def test_clasificar():
    m = DecisionTreeClassifier(random_state=0).fit(X, y)
    assert modulo.clasificar(m, [12, 5]) == 0
    assert isinstance(modulo.clasificar(m, [12, 5]), int)


def test_importancias():
    m = DecisionTreeClassifier(random_state=0).fit(X, y)
    imp = modulo.importancias(m)
    assert len(imp) == 2
    assert imp[0] == 1.0 and imp[1] == 0.0
