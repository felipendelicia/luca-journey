"""Tests del simulador de batalla (deterministas: el azar se inyecta)."""

from batalla_pokemon import tipos, estados, datos
from batalla_pokemon.modelos import Movimiento, Pokemon
from batalla_pokemon.batalla import Batalla, elegir_movimiento_cpu


# ----------------------------------------------------------------------
#  Tipos
# ----------------------------------------------------------------------
def test_efectividad_super():
    assert tipos.efectividad("agua", "fuego") == 2.0


def test_efectividad_poco():
    assert tipos.efectividad("fuego", "agua") == 0.5


def test_efectividad_normal():
    assert tipos.efectividad("normal", "fuego") == 1.0


# ----------------------------------------------------------------------
#  Movimiento y PP
# ----------------------------------------------------------------------
def test_movimiento_pp():
    m = Movimiento("Rayo", "electrico", 55, 2)
    assert m.usable() is True
    m.usar()
    assert m.pp == 1
    m.usar()
    assert m.usable() is False
    m.usar()  # no debería bajar de 0
    assert m.pp == 0


# ----------------------------------------------------------------------
#  Pokemon
# ----------------------------------------------------------------------
def test_pokemon_recibir_dano():
    p = Pokemon("Test", "normal", 50, [])
    p.recibir_dano(30)
    assert p.hp == 20
    p.recibir_dano(100)
    assert p.hp == 0
    assert p.esta_debilitado() is True


def test_pokemon_curar_no_supera_max():
    p = Pokemon("Test", "normal", 50, [])
    p.recibir_dano(40)
    p.curar(100)
    assert p.hp == 50


# ----------------------------------------------------------------------
#  Estados
# ----------------------------------------------------------------------
def test_aplicar_estado_una_vez():
    p = Pokemon("Test", "normal", 50, [])
    assert estados.aplicar_estado(p, estados.PARALIZADO) is True
    # Ya tiene estado: no se puede aplicar otro.
    assert estados.aplicar_estado(p, estados.DORMIDO) is False


def test_paralisis_bloquea_con_tirada_baja():
    p = Pokemon("Test", "normal", 50, [])
    estados.aplicar_estado(p, estados.PARALIZADO)
    puede, _ = estados.puede_atacar(p, tirada=0.1)  # < 0.25 -> bloqueado
    assert puede is False


def test_paralisis_permite_con_tirada_alta():
    p = Pokemon("Test", "normal", 50, [])
    estados.aplicar_estado(p, estados.PARALIZADO)
    puede, _ = estados.puede_atacar(p, tirada=0.9)
    assert puede is True


def test_dormido_se_despierta():
    p = Pokemon("Test", "normal", 50, [])
    estados.aplicar_estado(p, estados.DORMIDO, turnos_sueno=1)
    # Primer turno: descuenta a 0 y se despierta.
    puede, msg = estados.puede_atacar(p, tirada=0.5)
    assert puede is True
    assert p.estado is None


def test_veneno_hace_dano():
    p = Pokemon("Test", "normal", 80, [])
    estados.aplicar_estado(p, estados.ENVENENADO)
    dano, _ = estados.dano_por_estado(p)
    assert dano == 10  # 80 // 8
    assert p.hp == 70


# ----------------------------------------------------------------------
#  Batalla
# ----------------------------------------------------------------------
def _mov(nombre, tipo, poder, efecto=None, prob=0.0):
    return Movimiento(nombre, tipo, poder, 10, efecto=efecto, prob_efecto=prob)


def test_calcular_dano_con_efectividad():
    atacante = Pokemon("A", "agua", 100, [_mov("Agua", "agua", 40)])
    defensor = Pokemon("B", "fuego", 100, [])
    b = Batalla(atacante, defensor, rng=lambda: 0.9)
    dano, mult = b.calcular_dano(atacante.movimientos[0], defensor)
    assert mult == 2.0
    assert dano == 80  # 40 * 2


def test_ejecutar_movimiento_aplica_dano_y_pp():
    atacante = Pokemon("A", "agua", 100, [_mov("Agua", "agua", 40)])
    defensor = Pokemon("B", "fuego", 100, [])
    # rng alto: no se bloquea por estado, no proc de efecto.
    b = Batalla(atacante, defensor, rng=lambda: 0.99)
    b.ejecutar_movimiento(atacante, defensor, 0)
    assert defensor.hp == 20  # 100 - 80
    assert atacante.movimientos[0].pp == 9  # gastó 1 PP


def test_movimiento_aplica_estado_con_tirada_baja():
    # Usamos un rng que devuelve siempre 0.0: pasa la paralisis-check (0.0<0.25
    # significa bloqueo SOLO si estás paralizado; el atacante no lo está) y
    # hace proc del efecto (0.0 < prob).
    atacante = Pokemon("A", "electrico", 100, [_mov("Chispa", "electrico", 30, efecto=estados.PARALIZADO, prob=1.0)])
    defensor = Pokemon("B", "agua", 100, [])
    b = Batalla(atacante, defensor, rng=lambda: 0.0)
    b.ejecutar_movimiento(atacante, defensor, 0)
    assert defensor.estado == estados.PARALIZADO


def test_batalla_terminada_y_ganador():
    a = Pokemon("A", "normal", 100, [_mov("Golpe", "normal", 200)])
    bp = Pokemon("B", "normal", 100, [])
    b = Batalla(a, bp, rng=lambda: 0.99)
    assert b.terminada() is False
    b.ejecutar_movimiento(a, bp, 0)
    assert b.terminada() is True
    assert b.ganador() is a


def test_cpu_elige_movimiento_usable():
    p = Pokemon("CPU", "normal", 100, [
        Movimiento("Sin PP", "normal", 40, 0),   # no usable
        Movimiento("Con PP", "normal", 40, 5),   # usable
    ])
    indice = elegir_movimiento_cpu(p, rng=lambda: 0.0)
    assert indice == 1, "Debería elegir el único movimiento con PP"


def test_cpu_sin_movimientos_devuelve_none():
    p = Pokemon("CPU", "normal", 100, [Movimiento("X", "normal", 40, 0)])
    assert elegir_movimiento_cpu(p, rng=lambda: 0.0) is None


# ----------------------------------------------------------------------
#  Roster
# ----------------------------------------------------------------------
def test_roster_crea_pokemon():
    pikachu = datos.crear("Pikachu")
    assert pikachu is not None
    assert pikachu.nombre == "Pikachu"
    assert len(pikachu.movimientos) == 4


def test_roster_inexistente():
    assert datos.crear("Inventado") is None


def test_crear_da_objetos_distintos():
    # Dos llamadas no deben compartir el mismo objeto (PP independientes).
    a = datos.crear("Pikachu")
    b = datos.crear("Pikachu")
    a.movimientos[0].usar()
    assert a.movimientos[0].pp != b.movimientos[0].pp
