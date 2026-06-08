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


def union(a, b):
    return sorted(set(a) | set(b))


def diferencia(a, b):
    return sorted(set(a) - set(b))


def mismos_elementos(a, b):
    return set(a) == set(b)


def unicos(items):
    vistos = set()
    out = []
    for x in items:
        if x not in vistos:
            vistos.add(x)
            out.append(x)
    return out


def contar_distintos(items):
    return len(set(items))


def agrupar_por_inicial(palabras):
    d = {}
    for p in palabras:
        d.setdefault(p[0], []).append(p)
    return d


def invertir_dict(d):
    return {v: k for k, v in d.items()}


def claves_con_valor(d, v):
    return [k for k, val in d.items() if val == v]


def suma_valores(d):
    return sum(d.values())


def clave_mayor_valor(d):
    return max(d, key=lambda k: d[k])


def combinar_conteos(a, b):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, 0) + v
    return r


def son_anagramas(a, b):
    return sorted(a) == sorted(b)


def faltantes(esperados, tengo):
    return sorted(set(esperados) - set(tengo))


def aparece_una_vez(items):
    from collections import Counter
    c = Counter(items)
    return [x for x in items if c[x] == 1]


def tiene_todas(d, claves):
    return all(k in d for k in claves)


def dos_mas_comunes(items):
    from collections import Counter
    return [x for x, _ in Counter(items).most_common(2)]
