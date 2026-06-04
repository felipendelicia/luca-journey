"""
🧪 Tests — Semana 08: POO Introducción

Tests exhaustivos de la clase Pokemon, la clase Entrenador y las funciones.
Por defecto prueban soluciones.py.

    pytest semana-08-python-poo-introduccion/ -v
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana08_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar("soluciones")
Pokemon = modulo.Pokemon
Entrenador = modulo.Entrenador


# ----------------------------------------------------------------------
#  Clase Pokemon
# ----------------------------------------------------------------------
def test_init_guarda_atributos():
    p = Pokemon("Pikachu", "Electrico", 25)
    assert p.nombre == "Pikachu"
    assert p.tipo == "Electrico"
    assert p.nivel == 25
    assert p.hp == 100
    assert p.hp_max == 100


def test_str():
    p = Pokemon("Pikachu", "Electrico", 25)
    assert str(p) == "Pikachu (Electrico, Nivel 25)"


def test_repr():
    p = Pokemon("Pikachu", "Electrico", 25)
    assert repr(p) == "Pokemon('Pikachu', 'Electrico', 25)"


def test_atacar():
    p = Pokemon("Pikachu", "Electrico", 25)
    assert p.atacar() == "Pikachu ataca con un golpe de tipo Electrico!"


def test_recibir_dano():
    p = Pokemon("Pikachu", "Electrico", 25)
    p.recibir_dano(30)
    assert p.hp == 70


def test_recibir_dano_no_negativo():
    p = Pokemon("Pikachu", "Electrico", 25)
    p.recibir_dano(150)
    assert p.hp == 0, "El HP no debería bajar de 0"


def test_esta_debilitado():
    p = Pokemon("Pikachu", "Electrico", 25)
    assert p.esta_debilitado() is False
    p.recibir_dano(100)
    assert p.esta_debilitado() is True


def test_curar():
    p = Pokemon("Pikachu", "Electrico", 25)
    p.recibir_dano(50)   # hp = 50
    p.curar(20)          # hp = 70
    assert p.hp == 70


def test_curar_no_supera_maximo():
    p = Pokemon("Pikachu", "Electrico", 25)
    p.recibir_dano(10)   # hp = 90
    p.curar(50)          # intentaría 140
    assert p.hp == 100, "El HP no debería superar hp_max"


def test_subir_nivel():
    p = Pokemon("Pikachu", "Electrico", 25)
    p.subir_nivel()
    assert p.nivel == 26


def test_es_mas_fuerte_que():
    a = Pokemon("Charizard", "Fuego", 50)
    b = Pokemon("Pikachu", "Electrico", 25)
    assert a.es_mas_fuerte_que(b) is True
    assert b.es_mas_fuerte_que(a) is False


def test_porcentaje_hp():
    p = Pokemon("Pikachu", "Electrico", 25)
    assert p.porcentaje_hp() == 100
    p.recibir_dano(50)
    assert p.porcentaje_hp() == 50


# ----------------------------------------------------------------------
#  Clase Entrenador
# ----------------------------------------------------------------------
def test_entrenador_init():
    e = Entrenador("Ash")
    assert e.nombre == "Ash"
    assert e.equipo == []


def test_entrenador_agregar_y_cantidad():
    e = Entrenador("Ash")
    e.agregar(Pokemon("Pikachu", "Electrico", 25))
    e.agregar(Pokemon("Charizard", "Fuego", 50))
    assert e.cantidad() == 2


def test_entrenador_tiene_equipo():
    e = Entrenador("Ash")
    assert e.tiene_equipo() is False
    e.agregar(Pokemon("Pikachu", "Electrico", 25))
    assert e.tiene_equipo() is True


def test_entrenador_nombres():
    e = Entrenador("Ash")
    e.agregar(Pokemon("Pikachu", "Electrico", 25))
    e.agregar(Pokemon("Onix", "Roca", 30))
    assert e.nombres() == ["Pikachu", "Onix"]


def test_entrenador_nivel_total():
    e = Entrenador("Ash")
    e.agregar(Pokemon("Pikachu", "Electrico", 25))
    e.agregar(Pokemon("Charizard", "Fuego", 50))
    assert e.nivel_total() == 75


def test_entrenador_el_mas_fuerte():
    e = Entrenador("Ash")
    e.agregar(Pokemon("Pikachu", "Electrico", 25))
    fuerte = Pokemon("Charizard", "Fuego", 50)
    e.agregar(fuerte)
    assert e.el_mas_fuerte() is fuerte


def test_entrenador_el_mas_fuerte_vacio():
    e = Entrenador("Ash")
    assert e.el_mas_fuerte() is None, "Equipo vacío: el más fuerte es None"


# ----------------------------------------------------------------------
#  Funciones
# ----------------------------------------------------------------------
def test_crear_pokemon_inicial():
    p = modulo.crear_pokemon_inicial()
    assert isinstance(p, Pokemon)
    assert p.nombre == "Pikachu"
    assert p.nivel == 5


def test_batallar():
    atacante = Pokemon("Charizard", "Fuego", 50)
    defensor = Pokemon("Pikachu", "Electrico", 25)
    assert modulo.batallar(atacante, defensor, 30) is False, "70 HP: no debilitado"
    assert modulo.batallar(atacante, defensor, 100) is True, "0 HP: debilitado"


def test_contar_debilitados():
    a = Pokemon("A", "Normal", 10)
    b = Pokemon("B", "Normal", 10)
    b.recibir_dano(100)   # debilitado
    c = Pokemon("C", "Normal", 10)
    c.recibir_dano(100)   # debilitado
    assert modulo.contar_debilitados([a, b, c]) == 2
    assert modulo.contar_debilitados([]) == 0
