import ejercicios


def test_agrupar():
    modelo = ejercicios.agrupar(ejercicios.X_CLUSTER, 3)
    assert type(modelo).__name__ == "KMeans"
    assert modelo.n_clusters == 3


def test_etiquetas():
    modelo = ejercicios.agrupar(ejercicios.X_CLUSTER, 3)
    labs = ejercicios.etiquetas(modelo)
    assert len(labs) == 15
    # Los 3 grupos deben sumar 15
    assert labs.count(0) + labs.count(1) + labs.count(2) == 15
    # Cada grupo tiene exactamente 5 elementos (datos bien separados)
    assert sorted([labs.count(0), labs.count(1), labs.count(2)]) == [5, 5, 5]


def test_a_que_grupo():
    modelo = ejercicios.agrupar(ejercicios.X_CLUSTER, 3)
    g1 = ejercicios.a_que_grupo(modelo, [90, 35])
    g2 = ejercicios.a_que_grupo(modelo, [30, 90])
    g3 = ejercicios.a_que_grupo(modelo, [55, 55])
    # Los 3 puntos representan 3 clusters distintos
    assert len({g1, g2, g3}) == 3


def test_resumen_clusters():
    resultado = ejercicios.resumen_clusters(ejercicios.X_CLUSTER, 3)
    assert set(resultado.keys()) == {0, 1, 2}
    assert sorted(resultado.values()) == [5, 5, 5]
