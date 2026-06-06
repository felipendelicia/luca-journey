"""🔎 Soluciones — Búsqueda lineal y binaria"""


def busqueda_lineal(lista, x):
    for i, v in enumerate(lista):
        if v == x:
            return i
    return -1


def contiene(lista, x):
    return busqueda_lineal(lista, x) != -1


def busqueda_binaria(ordenada, x):
    lo, hi = 0, len(ordenada) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if ordenada[mid] == x:
            return mid
        if ordenada[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def primero_mayor(ordenada, x):
    for v in ordenada:
        if v > x:
            return v
    return None
