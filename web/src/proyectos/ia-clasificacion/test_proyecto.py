import ejercicios


def test_entrenar_clasificador():
    modelo = ejercicios.entrenar_clasificador(ejercicios.X_DATOS, ejercicios.Y_DATOS)
    assert type(modelo).__name__ == "KNeighborsClassifier"
    assert modelo.n_neighbors == 3


def test_clasificar():
    modelo = ejercicios.entrenar_clasificador(ejercicios.X_DATOS, ejercicios.Y_DATOS)
    assert ejercicios.clasificar(modelo, [84, 43, 78]) == 0
    assert ejercicios.clasificar(modelo, [40, 90, 30]) == 1


def test_clasificar_varios():
    modelo = ejercicios.entrenar_clasificador(ejercicios.X_DATOS, ejercicios.Y_DATOS)
    resultado = ejercicios.clasificar_varios(modelo, [[84, 43, 78], [40, 90, 30], [58, 62, 45]])
    assert resultado == [0, 1, 2]


def test_tipo_nombre():
    assert ejercicios.tipo_nombre(ejercicios.X_DATOS, ejercicios.Y_DATOS, [84, 43, 78]) == "Fuego"
    assert ejercicios.tipo_nombre(ejercicios.X_DATOS, ejercicios.Y_DATOS, [40, 90, 30]) == "Agua"
    assert ejercicios.tipo_nombre(ejercicios.X_DATOS, ejercicios.Y_DATOS, [58, 62, 45]) == "Planta"
