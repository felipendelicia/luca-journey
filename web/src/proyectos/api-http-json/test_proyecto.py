import ejercicios
import json


def test_armar_ficha():
    assert ejercicios.armar_ficha("Treecko", "planta", 5) == {"nombre": "Treecko", "tipo": "planta", "nivel": 5}
    assert ejercicios.armar_ficha("Geodude", "roca", 14) == {"nombre": "Geodude", "tipo": "roca", "nivel": 14}


def test_ficha_a_json():
    resultado = ejercicios.ficha_a_json("Mudkip", "agua", 5)
    assert isinstance(resultado, str)
    d = json.loads(resultado)
    assert d == {"nombre": "Mudkip", "tipo": "agua", "nivel": 5}


def test_json_a_ficha():
    assert ejercicios.json_a_ficha('{"nombre": "Ralts", "tipo": "psíquico", "nivel": 3}') == ("Ralts", "psíquico", 3)
    assert ejercicios.json_a_ficha('{"nombre": "Aron", "tipo": "acero", "nivel": 10}') == ("Aron", "acero", 10)


def test_filtrar_fichas():
    fichas = [
        {"nombre": "Geodude", "tipo": "roca", "nivel": 5},
        {"nombre": "Treecko", "tipo": "planta", "nivel": 5},
        {"nombre": "Nosepass", "tipo": "roca", "nivel": 8},
    ]
    assert ejercicios.filtrar_fichas(fichas, "roca") == ["Geodude", "Nosepass"]
    assert ejercicios.filtrar_fichas(fichas, "planta") == ["Treecko"]
    assert ejercicios.filtrar_fichas(fichas, "fuego") == []
