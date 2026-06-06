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
