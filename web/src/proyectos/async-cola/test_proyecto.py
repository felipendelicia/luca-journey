import ejercicios


def test_agregar():
    assert ejercicios.agregar([1, 2], 3) == [1, 2, 3]


def test_sacar():
    cola = [1, 2]
    assert ejercicios.sacar(cola) == 1
    assert cola == [2]
    assert ejercicios.sacar([]) is None


def test_vacia():
    assert ejercicios.vacia([]) is True
    assert ejercicios.vacia([1]) is False


def test_procesar():
    cola = [1, 2, 3]
    assert ejercicios.procesar(cola) == [1, 2, 3]
    assert cola == []
