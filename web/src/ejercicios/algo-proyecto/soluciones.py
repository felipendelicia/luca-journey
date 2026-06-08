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


def promedio_nivel(pokes):
    return sum(p["nivel"] for p in pokes) / len(pokes)


def nivel_maximo(pokes):
    return max(p["nivel"] for p in pokes)


def el_mas_fuerte(pokes):
    return max(pokes, key=lambda p: p["nivel"])


def filtrar_por_tipo(pokes, tipo):
    return [p for p in pokes if p["tipo"] == tipo]


def nombres(pokes):
    return [p["nombre"] for p in pokes]


def tipos_unicos(pokes):
    return sorted(set(p["tipo"] for p in pokes))


def existe(pokes, nombre):
    return any(p["nombre"] == nombre for p in pokes)


def nivel_de(pokes, nombre):
    for p in pokes:
        if p["nombre"] == nombre:
            return p["nivel"]
    return None


def subir_nivel_todos(pokes, n):
    return [{**p, "nivel": p["nivel"] + n} for p in pokes]


def mas_de_nivel(pokes, n):
    return [p for p in pokes if p["nivel"] > n]


def agrupar_por_tipo(pokes):
    d = {}
    for p in pokes:
        d.setdefault(p["tipo"], []).append(p["nombre"])
    return d


def ordenar_por_nombre(pokes):
    return [p["nombre"] for p in sorted(pokes, key=lambda p: p["nombre"])]


def tipo_mas_comun(pokes):
    from collections import Counter
    return Counter(p["tipo"] for p in pokes).most_common(1)[0][0]


def nivel_total(pokes):
    return sum(p["nivel"] for p in pokes)


def equipo_balanceado(pokes):
    tipos = [p["tipo"] for p in pokes]
    return len(set(tipos)) == len(tipos)


def contar(pokes):
    return len(pokes)
