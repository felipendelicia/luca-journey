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


def _arbol():
    return DecisionTreeClassifier(random_state=0).fit(X, y)


def test_precision():
    assert modulo.precision(_arbol(), X, y) == 1.0


def test_profundidad():
    assert modulo.profundidad(_arbol()) == 1


def test_cantidad_hojas():
    assert modulo.cantidad_hojas(_arbol()) == 2


def test_importancias_lista():
    assert modulo.importancias_lista(_arbol()) == [1.0, 0.0]


def test_feature_mas_importante():
    assert modulo.feature_mas_importante(_arbol()) == 0


def test_entrenar_con_profundidad():
    m = modulo.entrenar_con_profundidad(X, y, 1)
    assert m.predict([[15, 5]]).tolist() == [0]


def test_clasificar_varios():
    assert modulo.clasificar_varios(_arbol(), [[15, 5], [35, 5]]) == [0, 1]


def test_cantidad_clases():
    assert modulo.cantidad_clases(y) == 2


def test_contar_por_clase():
    assert modulo.contar_por_clase(y) == {0: 2, 1: 2}


def test_clase_mayoritaria():
    assert modulo.clase_mayoritaria(np.array([0, 0, 1])) == 0


def test_accuracy():
    assert modulo.accuracy([1, 0, 1], [1, 1, 1]) == 2 / 3


def test_cantidad_aciertos():
    assert modulo.cantidad_aciertos([1, 0, 1], [1, 1, 1]) == 2


def test_etiquetas_unicas():
    assert modulo.etiquetas_unicas(y) == [0, 1]


def test_cantidad_features():
    assert modulo.cantidad_features(X) == 2


def test_cantidad_muestras():
    assert modulo.cantidad_muestras(X) == 4


def test_predecir_y_contar():
    assert modulo.predecir_y_contar(_arbol(), X) == {0: 2, 1: 2}


def test_hay_clase():
    assert modulo.hay_clase(y, 1) is True
    assert modulo.hay_clase(y, 9) is False
