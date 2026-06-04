"""🧪 Tests — ML: clustering"""
import importlib.util
import os

import numpy as np
from sklearn.cluster import KMeans

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"iaclus_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))

# dos grupos bien separados
X = np.array([[0, 0], [1, 1], [0, 1], [10, 10], [11, 11], [10, 11]])


def test_agrupar():
    m = modulo.agrupar(X, 2)
    assert isinstance(m, KMeans)
    assert m.n_clusters == 2


def test_etiquetas():
    m = KMeans(n_clusters=2, random_state=0, n_init=10).fit(X)
    et = modulo.etiquetas(m)
    assert len(et) == 6
    # los 3 primeros van juntos, y los 3 últimos juntos, pero en grupo distinto
    assert et[0] == et[1] == et[2]
    assert et[3] == et[4] == et[5]
    assert et[0] != et[3]


def test_a_que_grupo():
    m = KMeans(n_clusters=2, random_state=0, n_init=10).fit(X)
    # un punto cercano al primer grupo debe caer en el grupo de los primeros
    assert modulo.a_que_grupo(m, [0.5, 0.5]) == int(m.labels_[0])
