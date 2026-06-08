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


def tamano(cola):
    return len(cola)


def esta_vacia(cola):
    return len(cola) == 0


def espacio_libre(cola, capacidad):
    return capacidad - len(cola)


def cabe(cola, capacidad):
    return len(cola) < capacidad


def esta_llena(cola, capacidad):
    return len(cola) >= capacidad


def encolar_varios(cola, items):
    for x in items:
        cola.append(x)
    return cola


def desencolar_varios(cola, n):
    out = []
    for _ in range(n):
        if cola:
            out.append(cola.pop(0))
    return out


def proximos(cola, n):
    return cola[:n]


def hay(cola, item):
    return item in cola


def posicion(cola, item):
    for i, x in enumerate(cola):
        if x == item:
            return i + 1
    return -1


def contar(cola, item):
    return cola.count(item)


def rotar(cola, n):
    for _ in range(n):
        if cola:
            cola.append(cola.pop(0))
    return cola


def dividir_en_lotes(items, tam):
    return [items[i:i + tam] for i in range(0, len(items), tam)]


def procesar_todos(cola, func):
    return [func(x) for x in cola]


def invertir_cola(cola):
    return cola[::-1]


def mover_al_final(cola, item):
    if item in cola:
        cola.remove(item)
        cola.append(item)
    return cola
