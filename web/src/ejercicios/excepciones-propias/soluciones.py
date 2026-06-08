"""✅ Soluciones — Excepciones personalizadas"""


class EquipoLlenoError(Exception):
    def __init__(self):
        super().__init__("equipo lleno")


class EntrenadorError(Exception):
    def __init__(self, mensaje, codigo):
        super().__init__(mensaje)
        self.codigo = codigo


def agregar(equipo, pokemon):
    if len(equipo) >= 6:
        raise EquipoLlenoError()
    equipo.append(pokemon)
    return equipo


def fallar(codigo):
    raise EntrenadorError("acceso denegado", codigo)


class HPInvalidoError(Exception):
    pass


class NivelInvalidoError(Exception):
    pass


class SaldoInsuficienteError(Exception):
    pass


class PokemonNoEncontradoError(Exception):
    pass


def validar_hp(hp):
    if hp < 0 or hp > 100:
        raise HPInvalidoError("hp fuera de 0..100")
    return hp


def validar_nivel(nivel):
    if nivel < 1 or nivel > 100:
        raise NivelInvalidoError("nivel fuera de 1..100")
    return nivel


def retirar(saldo, monto):
    if monto > saldo:
        raise SaldoInsuficienteError("saldo insuficiente")
    return saldo - monto


def buscar_pokemon(pokedex, nombre):
    if nombre not in pokedex:
        raise PokemonNoEncontradoError(nombre)
    return pokedex[nombre]


class RangoError(Exception):
    def __init__(self, valor):
        super().__init__(f"valor fuera de rango: {valor}")
        self.valor = valor


def validar_en_rango(n, lo, hi):
    if n < lo or n > hi:
        raise RangoError(n)
    return n


def nombre_del_error(func, x):
    try:
        func(x)
        return None
    except Exception as e:
        return type(e).__name__


def mensaje_de(error):
    return str(error)


def es_instancia(error, clase):
    return isinstance(error, clase)


def lanza_ese_error(func, x, clase):
    try:
        func(x)
        return False
    except clase:
        return True
    except Exception:
        return False


class ColeccionVaciaError(Exception):
    pass


def sacar_uno(coleccion):
    if len(coleccion) == 0:
        raise ColeccionVaciaError("la colección está vacía")
    return coleccion.pop()
