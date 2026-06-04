"""
🧪 combates/test_combates.py — Tests de los Combates de Gimnasio.

Por defecto prueban soluciones.py (el curso queda verde). La Liga los corre con
CURSO_MODULO=desafios para evaluar el trabajo del alumno, y filtra por gimnasio
con -k (ej: -k roca).

Cada test lleva el nombre del gimnasio (roca, cascada, ...) para poder filtrarlos.
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"combates_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


# 🪨 ROCA
def test_roca_organizar_por_extension():
    r = modulo.organizar_por_extension(["a.txt", "b.txt", "c.py", "LICENSE"])
    assert r == {"txt": 2, "py": 1, "sin_extension": 1}, (
        "Debería contar archivos por extensión (sin punto = 'sin_extension')"
    )


# 💧 CASCADA
def test_cascada_simular_duelo():
    assert modulo.simular_duelo(100, 100, 30, 20) == "a", "A pega más fuerte y empieza"
    assert modulo.simular_duelo(50, 100, 10, 60) == "b", "B pega muy fuerte"


# ⚡ TRUENO
def test_trueno_aplicar_n_veces():
    doble = lambda x: x * 2
    assert modulo.aplicar_n_veces(doble, 1, 3) == 8, "doble aplicado 3 veces a 1 = 8"
    assert modulo.aplicar_n_veces(doble, 5, 0) == 5, "0 veces no cambia el valor"


# 🌈 ARCOÍRIS
def test_arcoiris_parsear_equipo():
    texto = "Pikachu,Electrico,25\n\nOnix,Roca,30\n"
    r = modulo.parsear_equipo(texto)
    assert r == [
        {"nombre": "Pikachu", "tipo": "Electrico", "nivel": 25},
        {"nombre": "Onix", "tipo": "Roca", "nivel": 30},
    ], "Debería parsear las líneas (ignorando vacías) con nivel int"


# 💜 ALMA
def test_alma_mochila():
    m = modulo.Mochila()
    m.agregar("pocion", 3)
    assert m.cantidad("pocion") == 3
    assert m.usar("pocion") is True
    assert m.cantidad("pocion") == 2
    assert m.usar("revivir") is False, "Usar algo que no hay devuelve False"


# 🔮 PANTANO
def test_pantano_estadisticas():
    r = modulo.estadisticas([10, 20, 30])
    assert r == {"suma": 60, "promedio": 20, "maximo": 30, "minimo": 10}


def test_pantano_estadisticas_vacio():
    r = modulo.estadisticas([])
    assert r == {"suma": 0, "promedio": 0, "maximo": None, "minimo": None}


# 🌋 VOLCÁN
def test_volcan_sin_tipos_repetidos():
    pokemones = [
        {"nombre": "Charizard", "tipo": "Fuego"},
        {"nombre": "Magmar", "tipo": "Fuego"},
        {"nombre": "Blastoise", "tipo": "Agua"},
    ]
    assert modulo.equipo_sin_tipos_repetidos(pokemones) == ["Charizard", "Blastoise"]


# 🌍 TIERRA
def test_tierra_resumen_entrenador():
    r = modulo.resumen_entrenador(
        ["Pikachu", "Onix"], ["gano", "gano", "perdio", "perdio"]
    )
    assert r == {"total": 2, "victorias": 2, "porcentaje": 50}


def test_tierra_resumen_sin_batallas():
    r = modulo.resumen_entrenador(["Pikachu"], [])
    assert r == {"total": 1, "victorias": 0, "porcentaje": 0}
