"""
🧪 Tests de la Pokédex con Persistencia — Semana 07
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


interactivo = _cargar("interactivo")


def test_guardar_y_cargar_ciclo(tmp_path):
    ruta = str(tmp_path / "pokedex.csv")
    pokedex = [
        {"nombre": "Pikachu", "tipo": "Electrico", "nivel": 25},
        {"nombre": "Charizard", "tipo": "Fuego", "nivel": 50},
    ]
    interactivo.guardar_pokedex(ruta, pokedex)
    cargada = interactivo.cargar_pokedex(ruta)
    assert cargada == pokedex, "Lo guardado debería cargarse igual"


def test_cargar_inexistente_devuelve_vacio(tmp_path):
    ruta = str(tmp_path / "no_existe.csv")
    assert interactivo.cargar_pokedex(ruta) == [], (
        "Cargar un archivo inexistente debería devolver una lista vacía"
    )


def test_nivel_se_carga_como_entero(tmp_path):
    ruta = str(tmp_path / "p.csv")
    interactivo.guardar_pokedex(ruta, [{"nombre": "Onix", "tipo": "Roca", "nivel": 30}])
    cargada = interactivo.cargar_pokedex(ruta)
    assert isinstance(cargada[0]["nivel"], int), "El nivel debería cargarse como int"


def test_agregar_a_pokedex():
    pokedex = []
    interactivo.agregar_a_pokedex(pokedex, "Pikachu", "Electrico", 25)
    assert len(pokedex) == 1
    assert pokedex[0]["nombre"] == "Pikachu"


def test_csv_ejemplo_existe_y_carga():
    # El archivo de ejemplo de la carpeta data/ debería cargarse bien.
    ruta = os.path.join(_DIR, "data", "pokedex_ejemplo.csv")
    cargada = interactivo.cargar_pokedex(ruta)
    assert len(cargada) >= 5, "El CSV de ejemplo debería tener varios Pokémon"
    nombres = [p["nombre"] for p in cargada]
    assert "Pikachu" in nombres
