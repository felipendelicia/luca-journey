"""
🧪 Tests — Semana 04: Control de Flujo

Por defecto prueban soluciones.py. Para probar tu trabajo, cambiá abajo
_cargar("soluciones") por _cargar("ejercicios").

    pytest semana-04-python-control-de-flujo/ -v
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana04_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar("soluciones")


def test_puede_evolucionar():
    assert modulo.puede_evolucionar(25) is True, "Nivel 25 debería poder evolucionar"
    assert modulo.puede_evolucionar(24) is False, "Nivel 24 NO debería poder evolucionar"
    assert modulo.puede_evolucionar(99) is True


def test_estado_hp():
    assert modulo.estado_hp(100) == "sano", "HP 100 debería ser 'sano'"
    assert modulo.estado_hp(50) == "herido", "HP 50 debería ser 'herido'"
    assert modulo.estado_hp(10) == "grave", "HP 10 debería ser 'grave'"
    assert modulo.estado_hp(0) == "debilitado", "HP 0 debería ser 'debilitado'"


def test_ventaja_tipo():
    assert modulo.ventaja_tipo("agua", "fuego") is True, "Agua gana a Fuego"
    assert modulo.ventaja_tipo("fuego", "planta") is True, "Fuego gana a Planta"
    assert modulo.ventaja_tipo("planta", "agua") is True, "Planta gana a Agua"
    assert modulo.ventaja_tipo("electrico", "agua") is True, "Eléctrico gana a Agua"
    assert modulo.ventaja_tipo("fuego", "agua") is False, "Fuego NO gana a Agua"


def test_el_mas_fuerte():
    assert modulo.el_mas_fuerte(50, 80) == 80
    assert modulo.el_mas_fuerte(90, 30) == 90
    assert modulo.el_mas_fuerte(40, 40) == 40, "Si empatan, devolver el primero"


def test_clasificar_nivel():
    assert modulo.clasificar_nivel(5) == "novato"
    assert modulo.clasificar_nivel(20) == "intermedio"
    assert modulo.clasificar_nivel(50) == "experto"


def test_necesita_curarse():
    assert modulo.necesita_curarse(20) is True
    assert modulo.necesita_curarse(30) is False
    assert modulo.necesita_curarse(0) is True


def test_resultado_combate():
    assert modulo.resultado_combate(100, 50) == "ganaste"
    assert modulo.resultado_combate(20, 80) == "perdiste"
    assert modulo.resultado_combate(60, 60) == "empate"


def test_cuenta_regresiva():
    assert modulo.cuenta_regresiva(3) == "3,2,1,Ya!", (
        "cuenta_regresiva(3) debería ser '3,2,1,Ya!'"
    )
    assert modulo.cuenta_regresiva(1) == "1,Ya!"


def test_suma_1_a_n():
    assert modulo.suma_1_a_n(5) == 15, "1+2+3+4+5 = 15"
    assert modulo.suma_1_a_n(1) == 1
    assert modulo.suma_1_a_n(10) == 55


def test_factorial():
    assert modulo.factorial(0) == 1, "factorial(0) = 1 por definición"
    assert modulo.factorial(1) == 1
    assert modulo.factorial(5) == 120, "5! = 120"


def test_contar_pares():
    assert modulo.contar_pares(10) == 5, "Pares hasta 10: 2,4,6,8,10 = 5"
    assert modulo.contar_pares(1) == 0
    assert modulo.contar_pares(2) == 1


def test_cuantos_turnos():
    assert modulo.cuantos_turnos(100, 30) == 4, "100 HP con 30 de daño = 4 turnos"
    assert modulo.cuantos_turnos(100, 100) == 1
    assert modulo.cuantos_turnos(50, 10) == 5


def test_potencia():
    assert modulo.potencia(2, 3) == 8, "2^3 = 8"
    assert modulo.potencia(5, 0) == 1, "Cualquier cosa^0 = 1"
    assert modulo.potencia(10, 2) == 100


def test_es_primo():
    assert modulo.es_primo(7) is True, "7 es primo"
    assert modulo.es_primo(4) is False, "4 no es primo"
    assert modulo.es_primo(1) is False, "1 no es primo"
    assert modulo.es_primo(2) is True, "2 es primo"


def test_primer_divisor():
    assert modulo.primer_divisor(15) == 3
    assert modulo.primer_divisor(7) == 7, "Un primo se divide primero por sí mismo"
    assert modulo.primer_divisor(8) == 2


def test_contar_vocales():
    assert modulo.contar_vocales("pikachu") == 3, "pikachu tiene i, a, u"
    assert modulo.contar_vocales("xyz") == 0


def test_mayor_de_tres():
    assert modulo.mayor_de_tres(1, 2, 3) == 3
    assert modulo.mayor_de_tres(9, 2, 5) == 9
    assert modulo.mayor_de_tres(4, 7, 1) == 7


def test_signo():
    assert modulo.signo(5) == "positivo"
    assert modulo.signo(-3) == "negativo"
    assert modulo.signo(0) == "cero"


def test_esta_en_equipo():
    equipo = ["Pikachu", "Charizard", "Snorlax"]
    assert modulo.esta_en_equipo(equipo, "Charizard") is True
    assert modulo.esta_en_equipo(equipo, "Mewtwo") is False
    assert modulo.esta_en_equipo([], "Pikachu") is False, "Equipo vacío: nadie está"


def test_contar_debilitados():
    assert modulo.contar_debilitados([100, 0, 50, -10, 0]) == 3
    assert modulo.contar_debilitados([100, 50]) == 0
    assert modulo.contar_debilitados([]) == 0, "Lista vacía: 0 debilitados"
