"""
🧪 Tests — Semana 05: Funciones

Por defecto prueban soluciones.py. Para tu trabajo, cambiá _cargar("soluciones")
por _cargar("ejercicios").

    pytest semana-05-python-funciones/ -v
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana05_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar("soluciones")


def test_calcular_dano():
    assert modulo.calcular_dano(50, 20) == 30
    assert modulo.calcular_dano(10, 50) == 0, "El daño nunca es negativo"


def test_velocidad_efectiva():
    assert modulo.velocidad_efectiva(40, 10) == 60, "40 + 10*2 = 60"


def test_nivel_por_experiencia():
    assert modulo.nivel_por_experiencia(250) == 2
    assert modulo.nivel_por_experiencia(99) == 0
    assert modulo.nivel_por_experiencia(500) == 5


def test_experiencia_para_nivel():
    assert modulo.experiencia_para_nivel(5) == 125, "5^3 = 125"
    assert modulo.experiencia_para_nivel(1) == 1


def test_saludar_entrenador_con_default():
    assert modulo.saludar_entrenador("Ash") == "Hola Ash de Pueblo Paleta", (
        "Sin ciudad, debería usar el valor por defecto 'Pueblo Paleta'"
    )


def test_saludar_entrenador_con_ciudad():
    assert modulo.saludar_entrenador("Brock", "Ciudad Plateada") == (
        "Hola Brock de Ciudad Plateada"
    )


def test_aplicar_pocion():
    assert modulo.aplicar_pocion(50, 100) == 70, "50 + 20 (default) = 70"
    assert modulo.aplicar_pocion(90, 100) == 100, "No debería superar el máximo"
    assert modulo.aplicar_pocion(50, 100, 40) == 90, "Con cura 40: 50 + 40 = 90"


def test_promedio_tres():
    assert modulo.promedio_tres(10, 20, 30) == 20


def test_total_stats():
    assert modulo.total_stats(100, 50, 40, 60) == 250


def test_clasificar_poder():
    assert modulo.clasificar_poder(150) == "debil"
    assert modulo.clasificar_poder(300) == "promedio"
    assert modulo.clasificar_poder(500) == "fuerte"


def test_calcular_dano_con_bonus():
    assert modulo.calcular_dano_con_bonus(50, 20) == 30, "Sin bonus: 50-20"
    assert modulo.calcular_dano_con_bonus(50, 20, 10) == 40, "Con bonus 10"
    assert modulo.calcular_dano_con_bonus(10, 50) == 0, "Mínimo 0"


def test_multiplicador_efectividad():
    assert modulo.multiplicador_efectividad(True) == 2.0
    assert modulo.multiplicador_efectividad(False) == 1.0
    assert modulo.multiplicador_efectividad() == 1.0, "Por defecto, no es súper"


def test_dano_final():
    # base = 50-20 = 30 ; super -> *2 -> 60
    assert modulo.dano_final(50, 20, True) == 60
    # base = 30 ; normal -> *1 -> 30
    assert modulo.dano_final(50, 20, False) == 30


def test_factorial_recursivo():
    assert modulo.factorial(0) == 1
    assert modulo.factorial(5) == 120


def test_suma_recursiva():
    assert modulo.suma_recursiva(3) == 6, "3+2+1 = 6"
    assert modulo.suma_recursiva(0) == 0
    assert modulo.suma_recursiva(10) == 55


def test_potencia_recursiva():
    assert modulo.potencia_recursiva(2, 3) == 8
    assert modulo.potencia_recursiva(5, 0) == 1


def test_cuenta_regresiva_recursiva():
    assert modulo.cuenta_regresiva_recursiva(3) == "3,2,1,Ya!"
    assert modulo.cuenta_regresiva_recursiva(0) == "Ya!"


def test_lambda_doble():
    assert modulo.doble(5) == 10


def test_lambda_al_cuadrado():
    assert modulo.al_cuadrado(4) == 16


def test_lambda_mayor():
    assert modulo.mayor(3, 8) == 8
    assert modulo.mayor(9, 2) == 9


def test_lambda_es_par():
    assert modulo.es_par(4) is True
    assert modulo.es_par(7) is False
