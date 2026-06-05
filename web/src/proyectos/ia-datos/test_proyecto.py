import ejercicios


def test_separar_columnas():
    X, y = ejercicios.separar_columnas(ejercicios.DATASET)
    assert X.shape == (12, 4)
    assert y.shape == (12,)
    assert float(y[0]) == 0.0
    assert float(y[3]) == 1.0
    assert float(y[6]) == 2.0


def test_dividir():
    X, y = ejercicios.separar_columnas(ejercicios.DATASET)
    X_train, X_test, y_train, y_test = ejercicios.dividir(X, y)
    assert len(X_train) == 9
    assert len(X_test) == 3
    assert len(y_train) == 9
    assert len(y_test) == 3


def test_escalar():
    X, _ = ejercicios.separar_columnas(ejercicios.DATASET)
    Xs = ejercicios.escalar(X)
    assert Xs.shape == (12, 4)
    assert abs(float(Xs[:, 0].mean())) < 1e-9


def test_preparar_datos():
    X_train, X_test, y_train, y_test = ejercicios.preparar_datos(ejercicios.DATASET)
    assert len(X_train) == 9
    assert len(X_test) == 3
    # X_train media ~0 por columna
    assert abs(float(X_train[:, 0].mean())) < 1e-9
