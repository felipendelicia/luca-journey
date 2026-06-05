import ejercicios


def test_preparar_pipeline():
    X_train, X_test, y_train, y_test = ejercicios.preparar_pipeline(
        ejercicios.POKEMONES, ejercicios.TIPOS
    )
    assert len(X_train) == 30
    assert len(X_test) == 10
    assert len(y_train) == 30
    assert len(y_test) == 10
    # X_train debería estar escalado (media ~0)
    assert abs(float(X_train[:, 0].mean())) < 1e-9


def test_entrenar_pipeline():
    X_train, X_test, y_train, y_test = ejercicios.preparar_pipeline(
        ejercicios.POKEMONES, ejercicios.TIPOS
    )
    modelo = ejercicios.entrenar_pipeline(X_train, y_train)
    assert type(modelo).__name__ == "KNeighborsClassifier"
    assert modelo.n_neighbors == 3


def test_evaluar_pipeline():
    X_train, X_test, y_train, y_test = ejercicios.preparar_pipeline(
        ejercicios.POKEMONES, ejercicios.TIPOS
    )
    modelo = ejercicios.entrenar_pipeline(X_train, y_train)
    exactitud, n = ejercicios.evaluar_pipeline(modelo, X_test, y_test)
    assert exactitud == 1.0
    assert n == 10


def test_predecir_tipo():
    assert ejercicios.predecir_tipo([56, 78, 55, 77, 49, 86]) == "Fuego"
    assert ejercicios.predecir_tipo([58, 51, 85, 60, 84, 48]) == "Agua"
    assert ejercicios.predecir_tipo([74, 57, 60, 59, 89, 46]) == "Planta"
    assert ejercicios.predecir_tipo([40, 69, 33, 71, 36, 107]) == "Electrico"


def test_pokedex_completa():
    resultado = ejercicios.pokedex_completa()
    assert resultado["exactitud_test"] == 1.0
    assert resultado["n_test"] == 10
    assert len(resultado["tipos_predichos"]) == 10
    assert set(resultado["tipos_predichos"]).issubset({"Fuego", "Agua", "Planta", "Electrico"})
