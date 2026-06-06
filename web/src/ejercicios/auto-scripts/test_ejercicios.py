"""🧪 Tests — Scripts y argumentos"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"auto_scripts_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_contar_argumentos():
    assert modulo.contar_argumentos(["bot.py", "--nivel", "30"]) == 2
    assert modulo.contar_argumentos(["bot.py"]) == 0
    assert modulo.contar_argumentos(["bot.py", "a", "b", "c"]) == 3


def test_flag_presente():
    assert modulo.flag_presente(["bot.py", "--shiny"], "--shiny") is True
    assert modulo.flag_presente(["bot.py"], "--shiny") is False


def test_valor_de():
    assert modulo.valor_de(["bot.py", "--nivel", "30"], "--nivel", "1") == "30"
    assert modulo.valor_de(["bot.py"], "--nivel", "1") == "1"
    assert modulo.valor_de(["bot.py", "--nivel"], "--nivel", "1") == "1"


def test_parsear():
    assert modulo.parsear(["--nivel", "30", "--shiny"]) == {"nivel": 30, "nombre": "Pikachu", "shiny": True}
    assert modulo.parsear([]) == {"nivel": 1, "nombre": "Pikachu", "shiny": False}
    assert modulo.parsear(["--nombre", "Eevee"]) == {"nivel": 1, "nombre": "Eevee", "shiny": False}
