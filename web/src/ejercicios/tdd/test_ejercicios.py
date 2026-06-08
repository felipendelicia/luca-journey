"""🧪 Tests — TDD: el test primero"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"tdd_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_es_palindromo():
    assert modulo.es_palindromo("oso") is True
    assert modulo.es_palindromo("gato") is False
    assert modulo.es_palindromo("ana") is True


def test_factorial():
    assert modulo.factorial(0) == 1
    assert modulo.factorial(1) == 1
    assert modulo.factorial(5) == 120


def test_contar_vocales():
    assert modulo.contar_vocales("pikachu") == 3
    assert modulo.contar_vocales("xyz") == 0
    assert modulo.contar_vocales("AEIOU") == 5


def test_contar_palabras():
    assert modulo.contar_palabras("atrapalos a todos") == 3
    assert modulo.contar_palabras("uno") == 1


def test_es_primo():
    assert modulo.es_primo(7) is True
    assert modulo.es_primo(8) is False
    assert modulo.es_primo(1) is False


def test_fizzbuzz():
    assert modulo.fizzbuzz(15) == "FizzBuzz"
    assert modulo.fizzbuzz(3) == "Fizz"
    assert modulo.fizzbuzz(5) == "Buzz"
    assert modulo.fizzbuzz(7) == "7"


def test_capitalizar():
    assert modulo.capitalizar("pIKAchu") == "Pikachu"


def test_suma_pares():
    assert modulo.suma_pares([1, 2, 3, 4]) == 6


def test_es_bisiesto():
    assert modulo.es_bisiesto(2024) is True
    assert modulo.es_bisiesto(1900) is False
    assert modulo.es_bisiesto(2000) is True


def test_contar_letra():
    assert modulo.contar_letra("pikachu", "a") == 1


def test_quitar_vocales():
    assert modulo.quitar_vocales("Pikachu") == "Pkch"


def test_promedio():
    assert modulo.promedio([2, 4, 6]) == 4.0


def test_repetir_cada():
    assert modulo.repetir_cada([1, 2]) == [1, 1, 2, 2]


def test_iniciales():
    assert modulo.iniciales("ash ketchum") == "AK"


def test_mas_largo():
    assert modulo.mas_largo(["pi", "onix", "eevee"]) == "eevee"


def test_son_anagramas():
    assert modulo.son_anagramas("roma", "amor") is True
    assert modulo.son_anagramas("ash", "gary") is False


def test_titulo():
    assert modulo.titulo("ciudad de plateada") == "Ciudad De Plateada"


def test_contar_mayusculas():
    assert modulo.contar_mayusculas("PiKaChU") == 4


def test_sin_repetidos():
    assert modulo.sin_repetidos([1, 2, 1, 3, 2]) == [1, 2, 3]


def test_es_creciente():
    assert modulo.es_creciente([1, 2, 3]) is True
    assert modulo.es_creciente([1, 1, 2]) is False
