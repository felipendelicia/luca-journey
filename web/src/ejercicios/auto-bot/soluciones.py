"""🤖 Soluciones — Automatizador (bot)"""


def normalizar(nombre):
    return nombre.strip().lower()


def filtrar_nivel(pokes, minimo):
    return [p for p in pokes if p["nivel"] >= minimo]


def agrupar_por_tipo(pokes):
    grupos = {}
    for p in pokes:
        grupos.setdefault(p["tipo"], []).append(p["nombre"])
    return grupos


def contar(pokes):
    return len(pokes)


def normalizar_lista(nombres):
    return [n.strip().lower() for n in nombres]


def quitar_duplicados(nombres):
    vistos = set()
    out = []
    for n in nombres:
        if n not in vistos:
            vistos.add(n)
            out.append(n)
    return out


def solo_nombres(pokes):
    return [p["nombre"] for p in pokes]


def ordenar_por_nivel(pokes):
    return sorted(pokes, key=lambda p: p["nivel"], reverse=True)


def el_de_mayor_nivel(pokes):
    return max(pokes, key=lambda p: p["nivel"])


def nivel_promedio(pokes):
    return sum(p["nivel"] for p in pokes) / len(pokes)


def tipos_unicos(pokes):
    return sorted(set(p["tipo"] for p in pokes))


def filtrar_tipo(pokes, tipo):
    return [p for p in pokes if p["tipo"] == tipo]


def subir_nivel(pokes, n):
    return [{**p, "nivel": p["nivel"] + n} for p in pokes]


def contar_por_tipo(pokes):
    d = {}
    for p in pokes:
        d[p["tipo"]] = d.get(p["tipo"], 0) + 1
    return d


def nombres_filtrados(pokes, minimo):
    return [p["nombre"] for p in pokes if p["nivel"] >= minimo]


def existe(pokes, nombre):
    objetivo = nombre.strip().lower()
    return any(p["nombre"].strip().lower() == objetivo for p in pokes)


def buscar(pokes, nombre):
    objetivo = nombre.strip().lower()
    for p in pokes:
        if p["nombre"].strip().lower() == objetivo:
            return p
    return None


def nivel_total(pokes):
    return sum(p["nivel"] for p in pokes)


def mapear_nombres(pokes, func):
    return [func(p["nombre"]) for p in pokes]


def agregar_slug(pokes):
    return [{**p, "slug": p["nombre"].strip().lower()} for p in pokes]
