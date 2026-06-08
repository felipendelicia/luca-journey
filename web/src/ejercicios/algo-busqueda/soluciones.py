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


def cuenta_apariciones(lista, x):
    n = 0
    for e in lista:
        if e == x:
            n += 1
    return n


def indice_minimo(lista):
    mi = 0
    for i in range(1, len(lista)):
        if lista[i] < lista[mi]:
            mi = i
    return mi


def indice_maximo(lista):
    ma = 0
    for i in range(1, len(lista)):
        if lista[i] > lista[ma]:
            ma = i
    return ma


def ultimo_indice(lista, x):
    ult = -1
    for i in range(len(lista)):
        if lista[i] == x:
            ult = i
    return ult


def todos_los_indices(lista, x):
    return [i for i in range(len(lista)) if lista[i] == x]


def primer_par(lista):
    for e in lista:
        if e % 2 == 0:
            return e
    return None


def hay_repetidos(lista):
    return len(set(lista)) != len(lista)


def primer_repetido(lista):
    vistos = set()
    for e in lista:
        if e in vistos:
            return e
        vistos.add(e)
    return None


def dos_que_suman(lista, objetivo):
    vistos = set()
    for e in lista:
        if objetivo - e in vistos:
            return True
        vistos.add(e)
    return False


def mas_cercano(lista, x):
    mejor = lista[0]
    for e in lista:
        if abs(e - x) < abs(mejor - x):
            mejor = e
    return mejor


def esta_ordenada(lista):
    for i in range(1, len(lista)):
        if lista[i] < lista[i - 1]:
            return False
    return True


def cuantos_menores(ordenada, x):
    n = 0
    for e in ordenada:
        if e < x:
            n += 1
    return n


def buscar_texto(texto, sub):
    m = len(sub)
    for i in range(len(texto) - m + 1):
        if texto[i:i + m] == sub:
            return i
    return -1


def contar_en_rango(lista, a, b):
    return sum(1 for e in lista if a <= e <= b)


def interseccion(a, b):
    bset = set(b)
    out = []
    for e in a:
        if e in bset and e not in out:
            out.append(e)
    return out


def posicion_para_insertar(ordenada, x):
    i = 0
    while i < len(ordenada) and ordenada[i] < x:
        i += 1
    return i
