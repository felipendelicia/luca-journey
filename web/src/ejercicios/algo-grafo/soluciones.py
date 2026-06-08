"""🕸️ Soluciones — Grafos"""


def vecinos(grafo, nodo):
    return grafo.get(nodo, [])


def grado(grafo, nodo):
    return len(vecinos(grafo, nodo))


def hay_arista(grafo, a, b):
    return b in vecinos(grafo, a)


def nodos(grafo):
    return sorted(grafo.keys())


def cantidad_nodos(grafo):
    return len(grafo)


def nodos_aislados(grafo):
    return [n for n in grafo if len(grafo[n]) == 0]


def grado_maximo(grafo):
    return max((len(v) for v in grafo.values()), default=0)


def nodo_mas_conectado(grafo):
    return max(grafo, key=lambda n: len(grafo[n]))


def grados(grafo):
    return {n: len(grafo[n]) for n in grafo}


def vecinos_comunes(grafo, a, b):
    vb = set(grafo.get(b, []))
    return [x for x in grafo.get(a, []) if x in vb]


def agregar_arista(grafo, a, b):
    grafo.setdefault(a, [])
    grafo.setdefault(b, [])
    if b not in grafo[a]:
        grafo[a].append(b)
    if a not in grafo[b]:
        grafo[b].append(a)
    return grafo


def quitar_nodo(grafo, n):
    grafo.pop(n, None)
    for k in grafo:
        if n in grafo[k]:
            grafo[k].remove(n)
    return grafo


def recorrido_bfs(grafo, origen):
    visitados = [origen]
    cola = [origen]
    while cola:
        actual = cola.pop(0)
        for v in grafo.get(actual, []):
            if v not in visitados:
                visitados.append(v)
                cola.append(v)
    return visitados


def recorrido_dfs(grafo, origen):
    visitados = []

    def visitar(n):
        visitados.append(n)
        for v in grafo.get(n, []):
            if v not in visitados:
                visitar(v)

    visitar(origen)
    return visitados


def hay_camino(grafo, a, b):
    return b in recorrido_bfs(grafo, a)


def distancia(grafo, origen, destino):
    if origen == destino:
        return 0
    visitados = {origen}
    cola = [(origen, 0)]
    while cola:
        actual, d = cola.pop(0)
        for v in grafo.get(actual, []):
            if v == destino:
                return d + 1
            if v not in visitados:
                visitados.add(v)
                cola.append((v, d + 1))
    return -1


def componente(grafo, origen):
    return sorted(recorrido_bfs(grafo, origen))


def alcanzables_en(grafo, origen, pasos):
    visitados = {origen}
    cola = [(origen, 0)]
    while cola:
        actual, d = cola.pop(0)
        if d == pasos:
            continue
        for v in grafo.get(actual, []):
            if v not in visitados:
                visitados.add(v)
                cola.append((v, d + 1))
    return sorted(visitados)


def es_hoja(grafo, nodo):
    return len(grafo.get(nodo, [])) == 1


def cantidad_conexiones(grafo):
    return sum(len(v) for v in grafo.values())
