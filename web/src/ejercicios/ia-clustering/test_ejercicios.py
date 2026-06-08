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


def _km():
    return KMeans(n_clusters=2, random_state=0, n_init=10).fit(X)


def test_cantidad_grupos():
    assert modulo.cantidad_grupos(_km()) == 2


def test_a_que_grupos():
    r = modulo.a_que_grupos(_km(), [[0, 0], [10, 10]])
    assert r[0] != r[1]


def test_tamano_grupos():
    assert sorted(modulo.tamano_grupos(_km()).values()) == [3, 3]


def test_mismo_grupo():
    m = _km()
    assert modulo.mismo_grupo(m, [0, 0], [1, 1]) is True
    assert modulo.mismo_grupo(m, [0, 0], [10, 10]) is False


def test_agrupar_con_k():
    assert modulo.agrupar_con_k(X, 2).n_clusters == 2


def test_distancia_euclidea():
    assert modulo.distancia_euclidea([0, 0], [3, 4]) == 5.0


def test_indice_mas_cercano():
    assert modulo.indice_mas_cercano([0, 0], [[10, 10], [1, 1]]) == 1


def test_cantidad_por_etiqueta():
    assert modulo.cantidad_por_etiqueta([0, 0, 1, 1, 1]) == {0: 2, 1: 3}


def test_grupos_distintos():
    assert modulo.grupos_distintos([0, 0, 1]) == [0, 1]


def test_grupo_mayoritario():
    assert modulo.grupo_mayoritario([0, 0, 1]) == 0


def test_cantidad_puntos_en():
    assert modulo.cantidad_puntos_en([0, 0, 1], 0) == 2


def test_promedio_de_grupo():
    Xg = np.array([[2, 2], [4, 4], [100, 100]])
    assert np.array_equal(modulo.promedio_de_grupo(Xg, [0, 0, 1], 0), np.array([3.0, 3.0]))


def test_cantidad_muestras():
    assert modulo.cantidad_muestras(X) == 6


def test_cantidad_features():
    assert modulo.cantidad_features(X) == 2


def test_centro_mas_cercano():
    m = _km()
    assert modulo.centro_mas_cercano(m, [0, 0]) == modulo.centro_mas_cercano(m, [1, 1])


def test_cantidad_grupos_usados():
    assert modulo.cantidad_grupos_usados([0, 0, 1, 1]) == 2


def test_inercia_positiva():
    assert modulo.inercia_positiva(_km()) is True
