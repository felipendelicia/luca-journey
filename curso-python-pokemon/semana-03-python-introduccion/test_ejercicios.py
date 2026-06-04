"""
🧪 Tests — Semana 03: Python Introducción

Por defecto, estos tests prueban soluciones.py (así el curso pasa pytest verde).
Para probar TU trabajo, cambiá abajo "soluciones" por "ejercicios".

Correr con:
    pytest semana-03-python-introduccion/ -v
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana03_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


# 👇 Cambiá "soluciones" por "ejercicios" para testear tu propio código.
modulo = _cargar("soluciones")


# ----------------------------------------------------------------------
#  Ejercicios sin input
# ----------------------------------------------------------------------
def test_saludo():
    assert modulo.saludo() == "¡Hola, mundo Pokémon!", (
        "saludo() debería devolver exactamente '¡Hola, mundo Pokémon!'"
    )


def test_mi_pokemon_favorito_es_texto():
    resultado = modulo.mi_pokemon_favorito()
    assert isinstance(resultado, str) and len(resultado) > 0, (
        "mi_pokemon_favorito() debería devolver un string no vacío"
    )


def test_doble_nivel():
    assert modulo.doble_nivel(25) == 50, "doble_nivel(25) debería dar 50"
    assert modulo.doble_nivel(0) == 0, "doble_nivel(0) debería dar 0"


def test_suma():
    assert modulo.suma(10, 5) == 15, "suma(10, 5) debería dar 15"
    assert modulo.suma(-3, 3) == 0, "suma(-3, 3) debería dar 0"


def test_resta():
    assert modulo.resta(10, 4) == 6, "resta(10, 4) debería dar 6"


def test_promedio_stats():
    assert modulo.promedio_stats(90, 90, 90) == 90, (
        "promedio_stats(90, 90, 90) debería dar 90"
    )
    assert modulo.promedio_stats(10, 20, 30) == 20, (
        "promedio_stats(10, 20, 30) debería dar 20"
    )


def test_a_entero():
    resultado = modulo.a_entero("25")
    assert resultado == 25, "a_entero('25') debería dar 25"
    assert isinstance(resultado, int), "a_entero debería devolver un int, no un str"


def test_a_texto():
    resultado = modulo.a_texto(25)
    assert resultado == "25", "a_texto(25) debería dar '25'"
    assert isinstance(resultado, str), "a_texto debería devolver un str"


def test_a_decimal():
    resultado = modulo.a_decimal("6.5")
    assert resultado == 6.5, "a_decimal('6.5') debería dar 6.5"
    assert isinstance(resultado, float), "a_decimal debería devolver un float"


def test_nombre_del_tipo():
    assert modulo.nombre_del_tipo(25) == "int", "El tipo de 25 es 'int'"
    assert modulo.nombre_del_tipo("hola") == "str", "El tipo de 'hola' es 'str'"
    assert modulo.nombre_del_tipo(6.5) == "float", "El tipo de 6.5 es 'float'"
    assert modulo.nombre_del_tipo(True) == "bool", "El tipo de True es 'bool'"


def test_presentacion():
    assert modulo.presentacion("Pikachu", 25) == "Mi Pikachu es nivel 25", (
        "presentacion('Pikachu', 25) debería dar 'Mi Pikachu es nivel 25'"
    )


def test_ficha():
    esperado = "Nombre: Pikachu\nTipo: Electrico\nNivel: 25"
    assert modulo.ficha("Pikachu", "Electrico", 25) == esperado, (
        "La ficha debería tener 3 líneas: Nombre, Tipo y Nivel"
    )


def test_hp_total():
    assert modulo.hp_total(100, 3) == 160, (
        "hp_total(100, 3) debería dar 160 (100 + 3*20)"
    )
    assert modulo.hp_total(50, 0) == 50, "Sin pociones, el HP no cambia"


def test_nivel_es_par():
    assert modulo.nivel_es_par(10) is True, "10 es par"
    assert modulo.nivel_es_par(7) is False, "7 es impar"


def test_fusionar_nombres():
    assert modulo.fusionar_nombres("Char", "izard") == "Charizard", (
        "fusionar_nombres('Char', 'izard') debería dar 'Charizard'"
    )


# ----------------------------------------------------------------------
#  Ejercicios con input() — simulamos lo que escribe el usuario con monkeypatch.
# ----------------------------------------------------------------------
def _simular_inputs(monkeypatch, respuestas):
    """Hace que input() devuelva, en orden, los valores de la lista 'respuestas'."""
    iterador = iter(respuestas)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(iterador))


def test_pedir_nombre_y_saludar(monkeypatch):
    _simular_inputs(monkeypatch, ["Pikachu"])
    assert modulo.pedir_nombre_y_saludar() == "¡Hola, Pikachu!", (
        "Con input 'Pikachu' debería devolver '¡Hola, Pikachu!'"
    )


def test_pedir_nivel_y_subir(monkeypatch):
    _simular_inputs(monkeypatch, ["25"])
    assert modulo.pedir_nivel_y_subir() == 26, (
        "Con input '25' debería devolver 26 (subió un nivel)"
    )


def test_pedir_dos_numeros_y_sumar(monkeypatch):
    _simular_inputs(monkeypatch, ["10", "5"])
    assert modulo.pedir_dos_numeros_y_sumar() == 15, (
        "Con inputs '10' y '5' debería devolver 15"
    )


def test_registrar_entrenador(monkeypatch):
    _simular_inputs(monkeypatch, ["Ash", "Pueblo Paleta"])
    assert modulo.registrar_entrenador() == "Soy Ash de Pueblo Paleta", (
        "Debería devolver 'Soy Ash de Pueblo Paleta'"
    )


def test_elegir_inicial(monkeypatch, capsys):
    _simular_inputs(monkeypatch, ["pikachu"])
    modulo.elegir_inicial()
    salida = capsys.readouterr().out
    assert "Elegiste a PIKACHU" in salida, (
        "Debería imprimir 'Elegiste a PIKACHU' (en mayúsculas)"
    )
