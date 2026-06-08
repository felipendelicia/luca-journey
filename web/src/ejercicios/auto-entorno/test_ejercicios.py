"""🧪 Tests — Variables de entorno y config"""
import pytest
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"auto_entorno_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_parsear_env():
    assert modulo.parsear_env("API=abc\n# nota\nDEBUG=1") == {"API": "abc", "DEBUG": "1"}
    assert modulo.parsear_env("") == {}


def test_obtener():
    assert modulo.obtener({"A": "1"}, "A", "0") == "1"
    assert modulo.obtener({}, "A", "0") == "0"


def test_es_verdadero():
    assert modulo.es_verdadero("TRUE") is True
    assert modulo.es_verdadero("si") is True
    assert modulo.es_verdadero("no") is False


def test_leer_entorno():
    os.environ["POKE_TEST_VAR"] = "rojo"
    assert modulo.leer_entorno("POKE_TEST_VAR", "azul") == "rojo"
    assert modulo.leer_entorno("NO_EXISTE_XYZ", "azul") == "azul"


def test_claves():
    assert modulo.claves({"A": "1", "B": "2"}) == ["A", "B"]


def test_valores():
    assert modulo.valores({"A": "1", "B": "2"}) == ["1", "2"]


def test_tiene_clave():
    assert modulo.tiene_clave({"A": "1"}, "A") is True
    assert modulo.tiene_clave({"A": "1"}, "Z") is False


def test_cantidad():
    assert modulo.cantidad({"A": "1", "B": "2"}) == 2


def test_serializar():
    assert modulo.serializar({"API": "abc", "DEBUG": "1"}) == "API=abc\nDEBUG=1"


def test_fusionar():
    assert modulo.fusionar({"A": "1", "B": "2"}, {"B": "9"}) == {"A": "1", "B": "9"}


def test_solo_con_prefijo():
    assert modulo.solo_con_prefijo({"APP_A": "1", "DB_X": "2"}, "APP_") == {"APP_A": "1"}


def test_a_entero():
    assert modulo.a_entero({"N": "25"}, "N", 0) == 25
    assert modulo.a_entero({"N": "pika"}, "N", -1) == -1
    assert modulo.a_entero({}, "N", 5) == 5


def test_requerir():
    assert modulo.requerir({"A": "1"}, "A") == "1"
    with pytest.raises(KeyError):
        modulo.requerir({}, "A")


def test_quitar_comillas():
    assert modulo.quitar_comillas('"abc"') == "abc"
    assert modulo.quitar_comillas("abc") == "abc"


def test_es_comentario():
    assert modulo.es_comentario("# nota") is True
    assert modulo.es_comentario("A=1") is False


def test_contar_validas():
    assert modulo.contar_validas("A=1\n# nota\n\nB=2") == 2


def test_mayusculas_claves():
    assert modulo.mayusculas_claves({"api": "1"}) == {"API": "1"}


def test_con_default_si_vacio():
    assert modulo.con_default_si_vacio({"A": "x"}, "A", "def") == "x"
    assert modulo.con_default_si_vacio({"A": ""}, "A", "def") == "def"
    assert modulo.con_default_si_vacio({}, "A", "def") == "def"


def test_claves_ordenadas():
    assert modulo.claves_ordenadas({"B": "2", "A": "1"}) == ["A", "B"]


def test_invertir():
    assert modulo.invertir({"A": "1", "B": "2"}) == {"1": "A", "2": "B"}
