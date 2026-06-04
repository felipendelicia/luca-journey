"""
🧪 Tests — Semana 09: POO Avanzado

Prueban herencia, polimorfismo, property, staticmethod, classmethod y abc.
Por defecto prueban soluciones.py.

    pytest semana-09-python-poo-avanzado/ -v
"""

import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana09_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


# Por defecto prueba soluciones.py; la Liga lo corre con CURSO_MODULO=ejercicios.
modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))
Pokemon = modulo.Pokemon
PokemonFuego = modulo.PokemonFuego
PokemonAgua = modulo.PokemonAgua
PokemonPlanta = modulo.PokemonPlanta
PokemonElectrico = modulo.PokemonElectrico


# ----------------------------------------------------------------------
#  Herencia y clase abstracta
# ----------------------------------------------------------------------
def test_clase_abstracta_no_se_instancia():
    # Pokemon es abstracta: instanciarla directo debería fallar.
    with pytest.raises(TypeError):
        Pokemon("X", 1)


def test_subclase_hereda_atributos():
    charizard = PokemonFuego("Charizard", 50)
    assert charizard.nombre == "Charizard"
    assert charizard.nivel == 50
    assert charizard.hp == 100, "El HP heredado del padre debería ser 100"
    assert charizard.tipo == "Fuego"


def test_super_inicializa_padre():
    # Si super() funcionó, hp_max viene del padre.
    p = PokemonAgua("Blastoise", 52)
    assert p.hp_max == 100


# ----------------------------------------------------------------------
#  Polimorfismo
# ----------------------------------------------------------------------
def test_atacar_polimorfico():
    assert PokemonFuego("Charizard", 50).atacar() == "Charizard usa Lanzallamas!"
    assert PokemonAgua("Blastoise", 52).atacar() == "Blastoise usa Pistola Agua!"
    assert PokemonPlanta("Venusaur", 53).atacar() == "Venusaur usa Latigo Cepa!"
    assert PokemonElectrico("Pikachu", 25).atacar() == "Pikachu usa Impactrueno!"


def test_describir_ataques():
    equipo = [PokemonFuego("Charizard", 50), PokemonAgua("Blastoise", 52)]
    resultado = modulo.describir_ataques(equipo)
    assert resultado == ["Charizard usa Lanzallamas!", "Blastoise usa Pistola Agua!"]


# ----------------------------------------------------------------------
#  Property hp
# ----------------------------------------------------------------------
def test_property_hp_getter():
    p = PokemonFuego("Charizard", 50)
    assert p.hp == 100


def test_property_hp_setter_no_negativo():
    p = PokemonFuego("Charizard", 50)
    p.hp = -50
    assert p.hp == 0, "El setter debería evitar HP negativo"


def test_property_hp_setter_no_supera_max():
    p = PokemonFuego("Charizard", 50)
    p.hp = 500
    assert p.hp == 100, "El setter no debería superar hp_max"


def test_recibir_dano_usa_property():
    p = PokemonFuego("Charizard", 50)
    p.recibir_dano(150)
    assert p.hp == 0


# ----------------------------------------------------------------------
#  staticmethod y classmethod
# ----------------------------------------------------------------------
def test_es_tipo_valido():
    assert Pokemon.es_tipo_valido("Fuego") is True
    assert Pokemon.es_tipo_valido("Pizza") is False


def test_recien_nacido_classmethod():
    # Llamado desde una subclase, debe devolver una instancia de esa subclase.
    bebe = PokemonElectrico.recien_nacido("Pichu")
    assert isinstance(bebe, PokemonElectrico)
    assert bebe.nivel == 1
    assert bebe.tipo == "Electrico"


# ----------------------------------------------------------------------
#  Ventajas de tipo
# ----------------------------------------------------------------------
def test_tiene_ventaja():
    fuego = PokemonFuego("Charizard", 50)
    planta = PokemonPlanta("Venusaur", 53)
    assert modulo.tiene_ventaja(fuego, planta) is True, "Fuego gana a Planta"
    assert modulo.tiene_ventaja(planta, fuego) is False


def test_multiplicador():
    fuego = PokemonFuego("Charizard", 50)
    planta = PokemonPlanta("Venusaur", 53)
    agua = PokemonAgua("Blastoise", 52)
    assert modulo.multiplicador(fuego, planta) == 2.0, "Ventaja: x2"
    assert modulo.multiplicador(fuego, agua) == 0.5, "Desventaja: x0.5"
    assert modulo.multiplicador(fuego, fuego) == 1.0, "Mismo tipo: x1"


# ----------------------------------------------------------------------
#  Fábrica y utilidades de equipo
# ----------------------------------------------------------------------
def test_crear_por_tipo():
    assert isinstance(modulo.crear_por_tipo("Fuego", "X", 10), PokemonFuego)
    assert isinstance(modulo.crear_por_tipo("Agua", "X", 10), PokemonAgua)
    assert modulo.crear_por_tipo("Roca", "X", 10) is None, "Tipo inválido: None"


def test_tipos_del_equipo():
    equipo = [PokemonFuego("A", 10), PokemonAgua("B", 10)]
    assert modulo.tipos_del_equipo(equipo) == ["Fuego", "Agua"]


def test_equipo_balanceado():
    balanceado = [PokemonFuego("A", 10), PokemonAgua("B", 10)]
    repetido = [PokemonFuego("A", 10), PokemonFuego("B", 10)]
    assert modulo.equipo_balanceado(balanceado) is True
    assert modulo.equipo_balanceado(repetido) is False


def test_batalla_simple_con_ventaja():
    fuego = PokemonFuego("Charizard", 50)
    planta = PokemonPlanta("Venusaur", 53)
    # 30 de daño x2 por ventaja = 60.
    dano = modulo.batalla_simple(fuego, planta, 30)
    assert dano == 60
    assert planta.hp == 40, "100 - 60 = 40"


def test_cantidad_por_tipo():
    equipo = [
        PokemonFuego("A", 10),
        PokemonFuego("B", 10),
        PokemonAgua("C", 10),
    ]
    assert modulo.cantidad_por_tipo(equipo, "Fuego") == 2
    assert modulo.cantidad_por_tipo(equipo, "Planta") == 0
