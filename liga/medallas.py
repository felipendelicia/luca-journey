"""
liga.medallas — Las 8 medallas de gimnasio.

Una medalla se gana cuando todas las semanas que pide su gimnasio están completas.
"""

from . import datos, progreso


def gimnasio_ganado(estado, gimnasio):
    """True si están completas TODAS las semanas que pide ese gimnasio."""
    return all(progreso.semana_completa(estado, sid) for sid in gimnasio["requiere"])


def medallas_disponibles(estado):
    """Lista de ids de gimnasios cuyos requisitos ya están cumplidos."""
    return [g["id"] for g in datos.GIMNASIOS if gimnasio_ganado(estado, g)]


def chequear_nuevas(estado):
    """
    Otorga las medallas recién ganadas (las agrega a estado["medallas"]).
    Devuelve la lista de los gimnasios (dicts) nuevos que se acaban de ganar.
    """
    nuevas = []
    for gimnasio in datos.GIMNASIOS:
        if gimnasio["id"] in estado["medallas"]:
            continue
        if gimnasio_ganado(estado, gimnasio):
            estado["medallas"].append(gimnasio["id"])
            nuevas.append(gimnasio)
    return nuevas


def gimnasio_por_id(gid):
    for g in datos.GIMNASIOS:
        if g["id"] == gid:
            return g
    return None


def es_campeon(estado):
    """True si conseguiste las 8 medallas."""
    return len(estado["medallas"]) >= len(datos.GIMNASIOS)
