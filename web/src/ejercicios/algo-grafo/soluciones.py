"""🕸️ Soluciones — Grafos"""


def vecinos(grafo, nodo):
    return grafo.get(nodo, [])


def grado(grafo, nodo):
    return len(vecinos(grafo, nodo))


def hay_arista(grafo, a, b):
    return b in vecinos(grafo, a)


def nodos(grafo):
    return sorted(grafo.keys())
