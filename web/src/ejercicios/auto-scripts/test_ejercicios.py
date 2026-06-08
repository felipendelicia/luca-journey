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


def test_primer_argumento():
    assert modulo.primer_argumento(["a", "b"]) == "a"
    assert modulo.primer_argumento([]) is None


def test_ultimo_argumento():
    assert modulo.ultimo_argumento(["a", "b"]) == "b"
    assert modulo.ultimo_argumento([]) is None


def test_es_flag():
    assert modulo.es_flag("--verbose") is True
    assert modulo.es_flag("archivo.txt") is False


def test_solo_flags():
    assert modulo.solo_flags(["-v", "f.txt", "--n"]) == ["-v", "--n"]


def test_sin_flags():
    assert modulo.sin_flags(["-v", "f.txt", "--n"]) == ["f.txt"]


def test_cantidad_flags():
    assert modulo.cantidad_flags(["-v", "f.txt", "--n"]) == 2


def test_contar_posicionales():
    assert modulo.contar_posicionales(["-v", "f.txt", "g.txt"]) == 2


def test_posicion_de():
    assert modulo.posicion_de(["a", "b", "c"], "b") == 1
    assert modulo.posicion_de(["a"], "z") == -1


def test_tiene_todas_las_flags():
    assert modulo.tiene_todas_las_flags(["-v", "-n"], ["-v", "-n"]) is True
    assert modulo.tiene_todas_las_flags(["-v"], ["-v", "-n"]) is False


def test_quitar_flag():
    assert modulo.quitar_flag(["-v", "f.txt", "-v"], "-v") == ["f.txt"]


def test_agregar_flag():
    assert modulo.agregar_flag(["-v"], "-n") == ["-v", "-n"]
    assert modulo.agregar_flag(["-v"], "-v") == ["-v"]


def test_normalizar_flag():
    assert modulo.normalizar_flag("--verbose") == "verbose"


def test_valor_con_igual():
    assert modulo.valor_con_igual(["--nivel=25"], "--nivel") == "25"
    assert modulo.valor_con_igual(["-v"], "--nivel") is None, "Si no está, devolvé None"


def test_juntar_argumentos():
    assert modulo.juntar_argumentos(["python", "bot.py", "-v"]) == "python bot.py -v"


def test_reemplazar_flag():
    assert modulo.reemplazar_flag(["-v", "-x"], "-v", "-w") == ["-w", "-x"]


def test_hay_flag_repetida():
    assert modulo.hay_flag_repetida(["-v", "f", "-v"]) is True
    assert modulo.hay_flag_repetida(["-v", "-n"]) is False
