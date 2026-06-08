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


def esta_vacia(cola):
    return len(cola) == 0


def tamano(cola):
    return len(cola)


def proximo(cola):
    return cola[0] if cola else None


def encolar_varios(cola, elementos):
    for e in elementos:
        cola.append(e)
    return cola


def atender_a_todos(cola):
    out = []
    while cola:
        out.append(cola.pop(0))
    return out


def atender_n(cola, n):
    out = []
    for _ in range(n):
        if cola:
            out.append(cola.pop(0))
    return out


def simular_cola(operaciones):
    cola = []
    for op in operaciones:
        if op == "dequeue":
            if cola:
                cola.pop(0)
        else:
            cola.append(int(op.split()[1]))
    return cola


def josephus(nombres, k):
    cola = list(nombres)
    while len(cola) > 1:
        for _ in range(k - 1):
            cola.append(cola.pop(0))
        cola.pop(0)
    return cola[0]


def invertir_cola(cola):
    pila = []
    while cola:
        pila.append(cola.pop(0))
    out = []
    while pila:
        out.append(pila.pop())
    return out


def intercalar(a, b):
    out = []
    while a or b:
        if a:
            out.append(a.pop(0))
        if b:
            out.append(b.pop(0))
    return out


def posicion_en_fila(cola, x):
    for i, e in enumerate(cola):
        if e == x:
            return i + 1
    return -1


def mover_al_final(cola, x):
    if x in cola:
        cola.remove(x)
        cola.append(x)
    return cola


def hay_en_cola(cola, x):
    return x in cola


def duplicar_cada(cola):
    out = []
    for e in cola:
        out.append(e)
        out.append(e)
    return out


def atender_hasta(cola, x):
    out = []
    while cola:
        e = cola.pop(0)
        out.append(e)
        if e == x:
            break
    return out


def rotar(cola, n):
    for _ in range(n):
        if cola:
            cola.append(cola.pop(0))
    return cola
