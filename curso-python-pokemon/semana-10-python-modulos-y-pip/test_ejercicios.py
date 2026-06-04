"""
🧪 Tests — Semana 10: Módulos y pip

NO requieren internet: los tests del interactivo usan datos falsos.
Por defecto prueban soluciones.py.

    pytest semana-10-python-modulos-y-pip/ -v
"""

import importlib.util
import os
import sys
from datetime import date

_DIR = os.path.dirname(__file__)
# Agregamos esta carpeta al path para que 'import pokeutils' funcione
# dentro de soluciones.py / ejercicios.py.
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana10_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar("soluciones")
pokeutils = _cargar("pokeutils")


# ----------------------------------------------------------------------
#  Ejercicios
# ----------------------------------------------------------------------
def test_raiz_cuadrada():
    assert modulo.raiz_cuadrada(16) == 4.0


def test_redondear_arriba():
    assert modulo.redondear_arriba(4.1) == 5
    assert modulo.redondear_arriba(4.0) == 4


def test_redondear_abajo():
    assert modulo.redondear_abajo(4.9) == 4


def test_pi_redondeado():
    assert modulo.pi_redondeado() == 3.14


def test_tirar_dado_en_rango():
    # Tiramos muchas veces: siempre entre 1 y 6.
    for _ in range(50):
        valor = modulo.tirar_dado()
        assert 1 <= valor <= 6, f"El dado dio {valor}, fuera de rango 1-6"


def test_pokemon_al_azar_pertenece():
    lista = ["Pikachu", "Onix", "Snorlax"]
    for _ in range(20):
        assert modulo.pokemon_al_azar(lista) in lista


def test_mezclar_no_modifica_original():
    original = ["a", "b", "c", "d"]
    copia_original = list(original)
    mezclada = modulo.mezclar(original)
    assert original == copia_original, "No debería modificar la lista original"
    assert sorted(mezclada) == sorted(original), "Debe tener los mismos elementos"


def test_fecha_hoy():
    assert modulo.fecha_hoy() == date.today().isoformat()


def test_a_json_y_de_json():
    datos = {"nombre": "Pikachu", "nivel": 25}
    texto = modulo.a_json(datos)
    assert isinstance(texto, str)
    recuperado = modulo.de_json(texto)
    assert recuperado == datos, "Ida y vuelta JSON debería conservar los datos"


def test_guardar_y_cargar_json(tmp_path):
    ruta = str(tmp_path / "pokemon.json")
    datos = {"nombre": "Charizard", "tipo": "Fuego", "nivel": 50}
    modulo.guardar_json(ruta, datos)
    cargado = modulo.cargar_json(ruta)
    assert cargado == datos


def test_nombre_archivo():
    assert modulo.nombre_archivo("/home/ash/pokedex.txt") == "pokedex.txt"


def test_existe(tmp_path):
    ruta = tmp_path / "existe.txt"
    ruta.write_text("hola")
    assert modulo.existe(str(ruta)) is True
    assert modulo.existe(str(tmp_path / "no.txt")) is False


def test_resumen_pokemon_usa_modulo():
    resultado = modulo.resumen_pokemon("pikachu", "Electrico", 25)
    assert "Pikachu" in resultado
    assert "Electrico" in resultado


# ----------------------------------------------------------------------
#  Módulo propio pokeutils
# ----------------------------------------------------------------------
def test_pokeutils_formatear_nombre():
    assert pokeutils.formatear_nombre("pikachu") == "Pikachu"


def test_pokeutils_es_legendario():
    assert pokeutils.es_legendario("Mewtwo") is True
    assert pokeutils.es_legendario("Rattata") is False


def test_pokeutils_tiene_ventaja():
    assert pokeutils.tiene_ventaja("fuego", "planta") is True
    assert pokeutils.tiene_ventaja("fuego", "agua") is False


def test_pokeutils_slug():
    assert pokeutils.slug("Mr Mime") == "mr-mime"
    assert pokeutils.slug("Pikachu") == "pikachu"


def test_pokeutils_resumen_legendario_tiene_estrella():
    resultado = pokeutils.resumen("mewtwo", "Psiquico", 70)
    assert "⭐" in resultado, "Un legendario debería tener una estrella en el resumen"
