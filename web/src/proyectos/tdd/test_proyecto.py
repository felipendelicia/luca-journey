import ejercicios


def test_invertir():
    assert ejercicios.invertir("pikachu") == "uhcakip"
    assert ejercicios.invertir("abc") == "cba"
    assert ejercicios.invertir("") == ""


def test_contar_vocales():
    assert ejercicios.contar_vocales("pikachu") == 3
    assert ejercicios.contar_vocales("Eevee") == 4
    assert ejercicios.contar_vocales("rhythm") == 0
    assert ejercicios.contar_vocales("") == 0


def test_es_palindromo():
    assert ejercicios.es_palindromo("aba") is True
    assert ejercicios.es_palindromo("ABA") is True
    assert ejercicios.es_palindromo("abc") is False
    assert ejercicios.es_palindromo("radar") is True
    assert ejercicios.es_palindromo("") is True


def test_resumir():
    assert ejercicios.resumir("aba") == {"largo": 3, "vocales": 2, "invertido": "aba", "palindromo": True}
    assert ejercicios.resumir("abc") == {"largo": 3, "vocales": 1, "invertido": "cba", "palindromo": False}
