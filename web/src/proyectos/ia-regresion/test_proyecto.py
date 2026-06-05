import ejercicios


def test_entrenar_regresion():
    modelo = ejercicios.entrenar_regresion(ejercicios.NIVELES, ejercicios.CP_REAL)
    assert type(modelo).__name__ == "LinearRegression"


def test_predecir_cp():
    modelo = ejercicios.entrenar_regresion(ejercicios.NIVELES, ejercicios.CP_REAL)
    assert abs(ejercicios.predecir_cp(modelo, [10]) - 45.0) < 0.01
    assert abs(ejercicios.predecir_cp(modelo, [50]) - 185.0) < 0.01


def test_coeficientes():
    modelo = ejercicios.entrenar_regresion(ejercicios.NIVELES, ejercicios.CP_REAL)
    pendiente, intercepto = ejercicios.coeficientes(modelo)
    assert abs(pendiente - 3.5) < 0.01
    assert abs(intercepto - 10.0) < 0.01


def test_cp_varios():
    resultado = ejercicios.cp_varios([10, 20, 30])
    assert resultado == [45.0, 80.0, 115.0]
