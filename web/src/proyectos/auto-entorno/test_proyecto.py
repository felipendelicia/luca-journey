import ejercicios


def test_comentario():
    assert ejercicios.es_comentario("# nota") is True
    assert ejercicios.es_comentario("   ") is True
    assert ejercicios.es_comentario("API=1") is False


def test_partir():
    assert ejercicios.partir("API = abc ") == ("API", "abc")
    assert ejercicios.partir("URL=http://a=b") == ("URL", "http://a=b")


def test_cargar():
    assert ejercicios.cargar("# config\nAPI=abc\nDEBUG=1") == {"API": "abc", "DEBUG": "1"}
    assert ejercicios.cargar("") == {}


def test_defectos():
    assert ejercicios.con_defectos({"DEBUG": "1"}, {"DEBUG": "0", "NIVEL": "info"}) == {"DEBUG": "1", "NIVEL": "info"}
