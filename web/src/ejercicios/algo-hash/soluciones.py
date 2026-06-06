"""🗂️ Soluciones — Diccionarios y sets"""


def frecuencias(items):
    f = {}
    for x in items:
        f[x] = f.get(x, 0) + 1
    return f


def sin_duplicados(items):
    vistos = set()
    out = []
    for x in items:
        if x not in vistos:
            vistos.add(x)
            out.append(x)
    return out


def mas_comun(items):
    f = frecuencias(items)
    return max(f, key=f.get)


def interseccion(a, b):
    return sorted(set(a) & set(b))
