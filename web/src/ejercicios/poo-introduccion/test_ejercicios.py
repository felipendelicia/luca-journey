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


# Por defecto prueba soluciones.py; la Liga lo corre con CURSO_MODULO=ejercicios.
modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))
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


def _equipo():
    return [
        modulo.Pokemon("Pikachu", "Electrico", 25),
        modulo.Pokemon("Charizard", "Fuego", 90),
        modulo.Pokemon("Vulpix", "Fuego", 18),
    ]


def test_nombres_de():
    assert modulo.nombres_de(_equipo()) == ["Pikachu", "Charizard", "Vulpix"]


def test_nivel_promedio():
    assert round(modulo.nivel_promedio(_equipo()), 2) == round((25 + 90 + 18) / 3, 2)


def test_hay_debilitado():
    eq = _equipo()
    assert modulo.hay_debilitado(eq) is False
    eq[0].recibir_dano(100)
    assert modulo.hay_debilitado(eq) is True


def test_curar_a_todos():
    eq = _equipo()
    eq[0].recibir_dano(50)
    modulo.curar_a_todos(eq)
    assert eq[0].hp == eq[0].hp_max


def test_subir_a_todos():
    eq = _equipo()
    modulo.subir_a_todos(eq)
    assert eq[0].nivel == 26


def test_total_hp():
    assert modulo.total_hp(_equipo()) == 300


def test_vivos():
    eq = _equipo()
    eq[0].recibir_dano(100)
    assert modulo.nombres_de(modulo.vivos(eq)) == ["Charizard", "Vulpix"]


def test_ordenar_por_nivel():
    assert modulo.nombres_de(modulo.ordenar_por_nivel(_equipo())) == ["Charizard", "Pikachu", "Vulpix"]


def test_clonar():
    p = modulo.Pokemon("Pikachu", "Electrico", 25)
    c = modulo.clonar(p)
    assert (c.nombre, c.tipo, c.nivel) == ("Pikachu", "Electrico", 25)
    assert c is not p, "Tiene que ser un objeto NUEVO, no el mismo"


def test_es_del_tipo():
    p = modulo.Pokemon("Charizard", "Fuego", 90)
    assert modulo.es_del_tipo(p, "Fuego") is True
    assert modulo.es_del_tipo(p, "Agua") is False


def test_contar_de_tipo():
    assert modulo.contar_de_tipo(_equipo(), "Fuego") == 2


def test_crear_equipo():
    eq = modulo.crear_equipo(["A", "B"], "Agua", 10)
    assert modulo.nombres_de(eq) == ["A", "B"]
    assert eq[0].tipo == "Agua"
    assert eq[1].nivel == 10


def test_promedio_hp():
    assert modulo.promedio_hp(_equipo()) == 100.0


def test_el_de_nombre():
    assert modulo.el_de_nombre(_equipo(), "Vulpix").nivel == 18
    assert modulo.el_de_nombre(_equipo(), "Mew") is None, "Si no está, devolvé None"


def test_mas_debil_del_equipo():
    assert modulo.mas_debil_del_equipo(_equipo()).nombre == "Vulpix"
    assert modulo.mas_debil_del_equipo([]) is None
