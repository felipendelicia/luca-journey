"""🧪 Tests — Ejecutar programas"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"auto_subprocess_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_armar_comando():
    assert modulo.armar_comando("git", {"--depth": 1}) == ["git", "--depth", "1"]
    assert modulo.armar_comando("ls", {}) == ["ls"]


def test_parsear_salida():
    assert modulo.parsear_salida("uno\n\n  dos  \n") == ["uno", "dos"]
    assert modulo.parsear_salida("") == []


def test_contar_lineas():
    assert modulo.contar_lineas("a\n\nb\n") == 2
    assert modulo.contar_lineas("") == 0


def test_estado():
    assert modulo.estado({"returncode": 0}) == "ok"
    assert modulo.estado({"returncode": 1}) == "error"


def test_comando_a_texto():
    assert modulo.comando_a_texto(["git", "clone", "url"]) == "git clone url"


def test_texto_a_comando():
    assert modulo.texto_a_comando("ls -la /home") == ["ls", "-la", "/home"]


def test_agregar_flag():
    assert modulo.agregar_flag(["ls"], "-la") == ["ls", "-la"]


def test_tiene_flag():
    assert modulo.tiene_flag(["ls", "-la"], "-la") is True
    assert modulo.tiene_flag(["ls"], "-la") is False


def test_nombre_programa():
    assert modulo.nombre_programa(["git", "clone"]) == "git"


def test_cantidad_argumentos():
    assert modulo.cantidad_argumentos(["git", "clone", "url"]) == 2


def test_primera_linea():
    assert modulo.primera_linea("\n  uno  \ndos") == "uno"
    assert modulo.primera_linea("\n\n") == ""


def test_ultima_linea():
    assert modulo.ultima_linea("uno\n  dos  \n") == "dos"


def test_lineas_con():
    assert modulo.lineas_con("ok: a\nerror: b\nok: c", "ok") == ["ok: a", "ok: c"]


def test_contar_lineas_con():
    assert modulo.contar_lineas_con("ok\nerror\nok", "ok") == 2


def test_exitoso():
    assert modulo.exitoso({"returncode": 0}) is True
    assert modulo.exitoso({"returncode": 1}) is False


def test_fallido():
    assert modulo.fallido({"returncode": 1}) is True
    assert modulo.fallido({"returncode": 0}) is False


def test_combinar():
    assert modulo.combinar("python", ["bot.py", "-v"]) == ["python", "bot.py", "-v"]


def test_ultima_columna():
    assert modulo.ultima_columna("pikachu 25 electrico") == "electrico"


def test_tabla_a_filas():
    assert modulo.tabla_a_filas("a 1\nb 2") == [["a", "1"], ["b", "2"]]


def test_quitar_vacias():
    assert modulo.quitar_vacias(["a", "", "  ", "b"]) == ["a", "b"]
