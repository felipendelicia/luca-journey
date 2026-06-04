"""
🧪 Tests — Semana 06: Listas y Colecciones

Incluye casos borde: listas vacías, elementos no encontrados, etc.
Por defecto prueba soluciones.py.

    pytest semana-06-python-listas-y-colecciones/ -v
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana06_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar("soluciones")


def test_primer_pokemon():
    assert modulo.primer_pokemon(["Pikachu", "Onix"]) == "Pikachu"


def test_primer_pokemon_vacio():
    assert modulo.primer_pokemon([]) is None, "Lista vacía debería devolver None"


def test_ultimo_pokemon():
    assert modulo.ultimo_pokemon(["Pikachu", "Onix"]) == "Onix"


def test_ultimo_pokemon_vacio():
    assert modulo.ultimo_pokemon([]) is None, "Lista vacía debería devolver None"


def test_agregar_pokemon():
    equipo = ["Pikachu"]
    resultado = modulo.agregar_pokemon(equipo, "Onix")
    assert resultado == ["Pikachu", "Onix"]


def test_cantidad_pokemon():
    assert modulo.cantidad_pokemon(["a", "b", "c"]) == 3
    assert modulo.cantidad_pokemon([]) == 0


def test_esta_en_equipo():
    assert modulo.esta_en_equipo(["Pikachu", "Onix"], "Onix") is True
    assert modulo.esta_en_equipo(["Pikachu"], "Mewtwo") is False
    assert modulo.esta_en_equipo([], "Pikachu") is False


def test_quitar_pokemon():
    assert modulo.quitar_pokemon(["Pikachu", "Onix"], "Pikachu") == ["Onix"]


def test_quitar_pokemon_inexistente_no_rompe():
    # Quitar algo que no está NO debería tirar error.
    assert modulo.quitar_pokemon(["Pikachu"], "Mewtwo") == ["Pikachu"]


def test_equipo_lleno():
    assert modulo.equipo_lleno(["a", "b", "c", "d", "e", "f"]) is True
    assert modulo.equipo_lleno(["a", "b"]) is False
    assert modulo.equipo_lleno([]) is False


def test_tipos_unicos():
    assert modulo.tipos_unicos(["Fuego", "Agua", "Fuego"]) == ["Agua", "Fuego"]
    assert modulo.tipos_unicos([]) == [], "Lista vacía: sin tipos"


def test_contar_apariciones():
    assert modulo.contar_apariciones(["a", "b", "a", "a"], "a") == 3
    assert modulo.contar_apariciones(["a", "b"], "z") == 0, "No encontrado: 0"


def test_promedio_niveles():
    assert modulo.promedio_niveles([10, 20, 30]) == 20
    assert modulo.promedio_niveles([]) == 0, "Lista vacía: promedio 0 (no error)"


def test_nivel_maximo():
    assert modulo.nivel_maximo([10, 50, 30]) == 50
    assert modulo.nivel_maximo([]) is None, "Lista vacía: None"


def test_nombres_en_mayuscula():
    assert modulo.nombres_en_mayuscula(["pikachu", "onix"]) == ["PIKACHU", "ONIX"]
    assert modulo.nombres_en_mayuscula([]) == []


def test_niveles_altos():
    assert modulo.niveles_altos([10, 50, 30, 60], 40) == [50, 60]
    assert modulo.niveles_altos([10, 20], 40) == [], "Ninguno cumple: lista vacía"


def test_equipo_numerado():
    assert modulo.equipo_numerado(["Pikachu", "Onix"]) == [(0, "Pikachu"), (1, "Onix")]


def test_crear_pokemon():
    p = modulo.crear_pokemon("Pikachu", "Electrico", 25)
    assert p == {"nombre": "Pikachu", "tipo": "Electrico", "nivel": 25}


def test_obtener_dato():
    p = {"nombre": "Pikachu", "nivel": 25}
    assert modulo.obtener_dato(p, "nombre") == "Pikachu"
    assert modulo.obtener_dato(p, "defensa") is None, "Clave inexistente: None"


def test_subir_nivel():
    p = {"nombre": "Pikachu", "nivel": 25}
    resultado = modulo.subir_nivel(p)
    assert resultado["nivel"] == 26


def test_nombres_de():
    pokemones = [{"nombre": "Pikachu"}, {"nombre": "Onix"}]
    assert modulo.nombres_de(pokemones) == ["Pikachu", "Onix"]
    assert modulo.nombres_de([]) == []


def test_nombres_por_tipo():
    pokemones = [
        {"nombre": "Pikachu", "tipo": "Electrico"},
        {"nombre": "Charizard", "tipo": "Fuego"},
        {"nombre": "Raichu", "tipo": "Electrico"},
    ]
    assert modulo.nombres_por_tipo(pokemones, "Electrico") == ["Pikachu", "Raichu"]
    assert modulo.nombres_por_tipo(pokemones, "Agua") == [], "Tipo sin coincidencias"


def test_nombres_por_nivel_desc():
    pokemones = [
        {"nombre": "Pikachu", "nivel": 25},
        {"nombre": "Charizard", "nivel": 50},
        {"nombre": "Onix", "nivel": 30},
    ]
    assert modulo.nombres_por_nivel_desc(pokemones) == ["Charizard", "Onix", "Pikachu"]
