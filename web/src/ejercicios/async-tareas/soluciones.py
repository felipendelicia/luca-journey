"""🧵 Soluciones — Repartir tareas"""


def repartir(tareas, n):
    buckets = [[] for _ in range(n)]
    for i, t in enumerate(tareas):
        buckets[i % n].append(t)
    return buckets


def carga_de(buckets):
    return [len(b) for b in buckets]


def worker_libre(cargas):
    return cargas.index(min(cargas))


def equilibrado(buckets):
    tam = [len(b) for b in buckets]
    return max(tam) - min(tam) <= 1


def total_tareas(buckets):
    return sum(len(b) for b in buckets)


def cargas(buckets):
    return [len(b) for b in buckets]


def mas_cargado(buckets):
    return max(range(len(buckets)), key=lambda i: len(buckets[i]))


def menos_cargado(buckets):
    return min(range(len(buckets)), key=lambda i: len(buckets[i]))


def promedio_carga(buckets):
    return total_tareas(buckets) / len(buckets)


def diferencia_carga(buckets):
    cs = [len(b) for b in buckets]
    return max(cs) - min(cs)


def repartir_round_robin(tareas, n):
    buckets = [[] for _ in range(n)]
    for i, t in enumerate(tareas):
        buckets[i % n].append(t)
    return buckets


def agregar_a_menos_cargado(buckets, tarea):
    buckets[menos_cargado(buckets)].append(tarea)
    return buckets


def todas_las_tareas(buckets):
    out = []
    for b in buckets:
        out.extend(b)
    return out


def quien_tiene(buckets, tarea):
    for i, b in enumerate(buckets):
        if tarea in b:
            return i
    return -1


def tareas_de(buckets, i):
    return buckets[i]


def cantidad_workers(buckets):
    return len(buckets)


def hay_vacio(buckets):
    return any(len(b) == 0 for b in buckets)


def mover_una(buckets, origen, destino):
    if buckets[origen]:
        buckets[destino].append(buckets[origen].pop(0))
    return buckets


def estan_equilibrados(buckets):
    return diferencia_carga(buckets) <= 1


def worker_mas_grande(buckets):
    return max(buckets, key=len)
