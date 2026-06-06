"""🚶 Soluciones — Cola (queue)"""


def encolar(cola, x):
    cola.append(x)
    return cola


def atender(cola):
    if not cola:
        return None
    return cola.pop(0)


def en_espera(cola):
    return len(cola)


def orden_de_atencion(cola):
    return list(cola)
