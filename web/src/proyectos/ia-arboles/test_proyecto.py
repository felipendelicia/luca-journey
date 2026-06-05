import ejercicios


def test_entrenar_arbol():
    arbol = ejercicios.entrenar_arbol(ejercicios.X_ARBOL, ejercicios.Y_ARBOL)
    assert type(arbol).__name__ == "DecisionTreeClassifier"
    assert arbol.random_state == 0


def test_clasificar_arbol():
    arbol = ejercicios.entrenar_arbol(ejercicios.X_ARBOL, ejercicios.Y_ARBOL)
    assert ejercicios.clasificar_arbol(arbol, [10, 45, 28]) == 0
    assert ejercicios.clasificar_arbol(arbol, [16, 55, 40]) == 1
    assert ejercicios.clasificar_arbol(arbol, [15, 60, 35]) == 0
    assert ejercicios.clasificar_arbol(arbol, [20, 65, 45]) == 1


def test_importancias():
    arbol = ejercicios.entrenar_arbol(ejercicios.X_ARBOL, ejercicios.Y_ARBOL)
    imps = ejercicios.importancias(arbol)
    assert len(imps) == 3
    assert abs(imps[0] - 1.0) < 1e-9
    assert abs(imps[1]) < 1e-9
    assert abs(imps[2]) < 1e-9


def test_analizar_equipo():
    resultado = ejercicios.analizar_equipo([[10, 45, 28], [16, 55, 40], [20, 65, 45], [8, 30, 25]])
    assert resultado == {"puede_evolucionar": 2, "no_puede": 2}
