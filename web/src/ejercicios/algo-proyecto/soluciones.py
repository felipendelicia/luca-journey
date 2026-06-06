"""🔶 Soluciones — Algoritmos sobre la Pokédex"""


def contar_tipos(pokes):
    f = {}
    for p in pokes:
        f[p["tipo"]] = f.get(p["tipo"], 0) + 1
    return f


def ordenar_por_nivel(pokes):
    return sorted(pokes, key=lambda p: p["nivel"], reverse=True)


def buscar(pokes, nombre):
    for p in pokes:
        if p["nombre"] == nombre:
            return p
    return None


def top_n(pokes, n):
    return [p["nombre"] for p in ordenar_por_nivel(pokes)[:n]]
