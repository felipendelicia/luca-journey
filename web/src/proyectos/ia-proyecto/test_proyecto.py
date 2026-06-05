import ejercicios


def test_preparar():
    X_train, X_test, y_train, y_test = ejercicios.preparar(
        ejercicios.POKEDEX_DATA, ejercicios.POKEDEX_TIPOS
    )
    assert len(X_train) == 27
    assert len(X_test) == 9
    assert len(y_train) == 27
    assert len(y_test) == 9


def test_entrenar_pokedex():
    X_train, X_test, y_train, y_test = ejercicios.preparar(
        ejercicios.POKEDEX_DATA, ejercicios.POKEDEX_TIPOS
    )
    modelo = ejercicios.entrenar_pokedex(X_train, y_train)
    assert type(modelo).__name__ == "KNeighborsClassifier"
    assert modelo.n_neighbors == 3


def test_evaluar_pokedex():
    X_train, X_test, y_train, y_test = ejercicios.preparar(
        ejercicios.POKEDEX_DATA, ejercicios.POKEDEX_TIPOS
    )
    modelo = ejercicios.entrenar_pokedex(X_train, y_train)
    acc = ejercicios.evaluar_pokedex(modelo, X_test, y_test)
    assert acc == 1.0


def test_identificar_tipo():
    assert ejercicios.identificar_tipo([45, 72, 43, 80]) == "Fuego"
    assert ejercicios.identificar_tipo([55, 50, 82, 40]) == "Agua"
    assert ejercicios.identificar_tipo([72, 55, 60, 45]) == "Planta"
    assert ejercicios.identificar_tipo([38, 60, 30, 98]) == "Electrico"
