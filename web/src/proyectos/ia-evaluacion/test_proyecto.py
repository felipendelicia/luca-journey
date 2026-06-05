import ejercicios


def test_calcular_precision():
    assert ejercicios.calcular_precision([0, 1, 1, 0], [0, 1, 0, 0]) == 0.75
    assert ejercicios.calcular_precision([0, 1, 2], [0, 1, 2]) == 1.0
    assert abs(ejercicios.calcular_precision([0, 1, 2], [1, 0, 2]) - 1/3) < 1e-9


def test_dividir_y_evaluar():
    resultado = ejercicios.dividir_y_evaluar(ejercicios.X_EVAL, ejercicios.Y_EVAL)
    assert resultado == 1.0


def test_score_modelo():
    from sklearn.neighbors import KNeighborsClassifier
    # Entrena con todos los datos y evalúa sobre los mismos (score máximo)
    modelo = KNeighborsClassifier(n_neighbors=1).fit(
        ejercicios.X_EVAL, ejercicios.Y_EVAL
    )
    s = ejercicios.score_modelo(modelo, ejercicios.X_EVAL, ejercicios.Y_EVAL)
    assert s == 1.0


def test_evaluar_completo():
    resultado = ejercicios.evaluar_completo(ejercicios.X_EVAL, ejercicios.Y_EVAL)
    assert resultado["n_test"] == 9
    assert resultado["precision"] == 1.0
