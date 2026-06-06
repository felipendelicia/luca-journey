"""🎟️ Soluciones — Cola productor/consumidor"""


def encolar(cola, item):
    cola.append(item)
    return cola


def desencolar(cola):
    if not cola:
        return None
    return cola.pop(0)


def siguiente(cola):
    return cola[0] if cola else None


def vaciar(cola):
    procesados = []
    while cola:
        procesados.append(cola.pop(0))
    return procesados
