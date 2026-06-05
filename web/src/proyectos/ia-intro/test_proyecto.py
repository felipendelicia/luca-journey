import ejercicios


def test_crear_modelo():
    modelo = ejercicios.crear_modelo()
    assert type(modelo).__name__ == "KNeighborsClassifier"
    assert modelo.n_neighbors == 1


def test_entrenar():
    modelo = ejercicios.crear_modelo()
    modelo2 = ejercicios.entrenar(modelo, ejercicios.X_TRAIN, ejercicios.Y_TRAIN)
    # Después de entrenar, el modelo puede predecir sin error
    pred = modelo2.predict([ejercicios.X_TRAIN[0]])
    assert len(pred) == 1


def test_predecir():
    modelo = ejercicios.crear_modelo()
    modelo = ejercicios.entrenar(modelo, ejercicios.X_TRAIN, ejercicios.Y_TRAIN)
    assert ejercicios.predecir(modelo, [88, 42]) == 0
    assert ejercicios.predecir(modelo, [41, 89]) == 1


def test_clasificador_completo():
    resultado = ejercicios.clasificador_completo(
        ejercicios.X_TRAIN, ejercicios.Y_TRAIN,
        [[88, 42], [41, 89], [80, 50]]
    )
    assert resultado == [0, 1, 0]
