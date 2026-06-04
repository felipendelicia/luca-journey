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
