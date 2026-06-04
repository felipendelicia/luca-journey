"""Tests del módulo pokedex_web.storage y pokedex_web.pokeapi (sin internet)."""

import os
import sys

# Aseguramos que el paquete sea importable aun si se corre suelto.
_DIR = os.path.dirname(os.path.dirname(__file__))
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)

from pokedex_web import storage, pokeapi


def test_cargar_inexistente(tmp_path):
    assert storage.cargar(str(tmp_path / "no.json")) == []


def test_agregar_asigna_id(tmp_path):
    ruta = str(tmp_path / "d.json")
    p1 = storage.agregar(ruta, {"nombre": "Pikachu", "tipo": "electric", "nivel": 25})
    p2 = storage.agregar(ruta, {"nombre": "Onix", "tipo": "rock", "nivel": 30})
    assert p1["id"] == 1
    assert p2["id"] == 2


def test_buscar_por_id(tmp_path):
    ruta = str(tmp_path / "d.json")
    p = storage.agregar(ruta, {"nombre": "Pikachu", "tipo": "electric", "nivel": 25})
    encontrado = storage.buscar_por_id(ruta, p["id"])
    assert encontrado["nombre"] == "Pikachu"
    assert storage.buscar_por_id(ruta, 999) is None


def test_eliminar(tmp_path):
    ruta = str(tmp_path / "d.json")
    p = storage.agregar(ruta, {"nombre": "Rattata", "tipo": "normal", "nivel": 5})
    assert storage.eliminar(ruta, p["id"]) is True
    assert storage.cargar(ruta) == []
    assert storage.eliminar(ruta, 999) is False


def test_proximo_id_vacio():
    assert storage.proximo_id([]) == 1


def test_pokeapi_parsear():
    datos_falsos = {
        "name": "pikachu",
        "height": 4,
        "weight": 60,
        "types": [{"type": {"name": "electric"}}],
    }
    info = pokeapi.parsear(datos_falsos)
    assert info["nombre"] == "Pikachu"
    assert info["altura"] == 0.4
    assert info["peso"] == 6.0
    assert info["tipo"] == "electric"
