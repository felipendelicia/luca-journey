"""🤖 Soluciones — Automatizador (bot)"""


def normalizar(nombre):
    return nombre.strip().lower()


def filtrar_nivel(pokes, minimo):
    return [p for p in pokes if p["nivel"] >= minimo]


def agrupar_por_tipo(pokes):
    grupos = {}
    for p in pokes:
        grupos.setdefault(p["tipo"], []).append(p["nombre"])
    return grupos


def contar(pokes):
    return len(pokes)
