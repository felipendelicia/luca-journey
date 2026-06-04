"""
🧪 Tests — Semana 07: Cadenas y Archivos

Los tests de archivos usan 'tmp_path' (una carpeta temporal que pytest crea
y borra sola). Por defecto prueban soluciones.py.

    pytest semana-07-python-cadenas-y-archivos/ -v
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana07_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


# Por defecto prueba soluciones.py; la Liga lo corre con CURSO_MODULO=ejercicios.
modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


# ----------------------------------------------------------------------
#  Strings
# ----------------------------------------------------------------------
def test_a_mayusculas():
    assert modulo.a_mayusculas("pikachu") == "PIKACHU"


def test_limpiar_espacios():
    assert modulo.limpiar_espacios("  Pikachu  ") == "Pikachu"


def test_reemplazar():
    assert modulo.reemplazar("Pikachu", "a", "@") == "Pik@chu"


def test_separar_csv():
    assert modulo.separar_csv("Pikachu,Electrico,25") == ["Pikachu", "Electrico", "25"]


def test_unir_csv():
    assert modulo.unir_csv(["Charizard", "Fuego", 50]) == "Charizard,Fuego,50"


def test_invertir():
    assert modulo.invertir("Pikachu") == "uhcakiP"


def test_cantidad_caracteres():
    assert modulo.cantidad_caracteres("Pikachu") == 7


def test_empieza_con():
    assert modulo.empieza_con("Pikachu", "Pika") is True
    assert modulo.empieza_con("Pikachu", "Char") is False


def test_primeras_letras():
    assert modulo.primeras_letras("Pikachu", 4) == "Pika"


def test_ultimas_letras():
    assert modulo.ultimas_letras("Pikachu", 3) == "chu"


def test_capitalizar():
    assert modulo.capitalizar("pikachu") == "Pikachu"
    assert modulo.capitalizar("CHARIZARD") == "Charizard"


def test_contar_subtexto():
    assert modulo.contar_subtexto("Pikachu", "a") == 1
    assert modulo.contar_subtexto("aaa", "a") == 3


def test_convertir_entero_seguro_ok():
    assert modulo.convertir_entero_seguro("25") == 25


def test_convertir_entero_seguro_falla():
    assert modulo.convertir_entero_seguro("abc") == 0, "Texto inválido: usa el default"
    assert modulo.convertir_entero_seguro("abc", default=-1) == -1


# ----------------------------------------------------------------------
#  Archivos (con tmp_path)
# ----------------------------------------------------------------------
def test_escribir_y_leer(tmp_path):
    ruta = tmp_path / "pokedex.txt"
    modulo.escribir_texto(str(ruta), "Pikachu")
    assert modulo.leer_texto(str(ruta)) == "Pikachu"


def test_escribir_reemplaza(tmp_path):
    ruta = tmp_path / "x.txt"
    modulo.escribir_texto(str(ruta), "viejo")
    modulo.escribir_texto(str(ruta), "nuevo")
    assert modulo.leer_texto(str(ruta)) == "nuevo", "El modo 'w' debe reemplazar"


def test_agregar_linea(tmp_path):
    ruta = tmp_path / "equipo.txt"
    modulo.agregar_linea(str(ruta), "Pikachu")
    modulo.agregar_linea(str(ruta), "Charizard")
    contenido = modulo.leer_texto(str(ruta))
    assert "Pikachu\n" in contenido
    assert "Charizard\n" in contenido


def test_contar_lineas(tmp_path):
    ruta = tmp_path / "lista.txt"
    modulo.escribir_texto(str(ruta), "a\nb\nc\n")
    assert modulo.contar_lineas(str(ruta)) == 3


def test_guardar_y_cargar_lista(tmp_path):
    ruta = tmp_path / "datos.txt"
    modulo.guardar_lista(str(ruta), ["Pikachu", "Onix", "Snorlax"])
    cargada = modulo.cargar_lista(str(ruta))
    assert cargada == ["Pikachu", "Onix", "Snorlax"]


def test_cargar_lista_archivo_inexistente(tmp_path):
    ruta = tmp_path / "no_existe.txt"
    assert modulo.cargar_lista(str(ruta)) == [], (
        "Si el archivo no existe, debería devolver lista vacía (no romper)"
    )


def test_parsear_pokemon():
    resultado = modulo.parsear_pokemon("Pikachu,Electrico,25")
    assert resultado == {"nombre": "Pikachu", "tipo": "Electrico", "nivel": 25}
    assert isinstance(resultado["nivel"], int), "El nivel debería ser un int"
