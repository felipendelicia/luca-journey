"""🔢 Soluciones — Ordenar listas"""


def indice_minimo(lista):
    idx = 0
    for i in range(1, len(lista)):
        if lista[i] < lista[idx]:
            idx = i
    return idx


def esta_ordenada(lista):
    return all(lista[i] <= lista[i + 1] for i in range(len(lista) - 1))


def ordenar_burbuja(lista):
    a = list(lista)
    for i in range(len(a)):
        for j in range(len(a) - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def ordenar_seleccion(lista):
    a = list(lista)
    for i in range(len(a)):
        m = i
        for j in range(i + 1, len(a)):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
    return a


def ordenar_insercion(lista):
    out = list(lista)
    for i in range(1, len(out)):
        actual = out[i]
        j = i - 1
        while j >= 0 and out[j] > actual:
            out[j + 1] = out[j]
            j -= 1
        out[j + 1] = actual
    return out


def ordenar_desc(lista):
    return sorted(lista, reverse=True)


def segundo_menor(lista):
    return sorted(lista)[1]


def mediana(lista):
    s = sorted(lista)
    n = len(s)
    m = n // 2
    if n % 2 == 1:
        return s[m]
    return (s[m - 1] + s[m]) / 2


def top_n(lista, n):
    return sorted(lista, reverse=True)[:n]


def ordenar_por_longitud(palabras):
    return sorted(palabras, key=len)


def mezclar_ordenadas(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def esta_ordenada_desc(lista):
    for i in range(1, len(lista)):
        if lista[i] > lista[i - 1]:
            return False
    return True


def unicos_ordenados(lista):
    return sorted(set(lista))


def invertir(lista):
    out = []
    for i in range(len(lista) - 1, -1, -1):
        out.append(lista[i])
    return out


def kesimo_menor(lista, k):
    return sorted(lista)[k - 1]


def ordenar_absoluto(lista):
    return sorted(lista, key=abs)


def contar_swaps_burbuja(lista):
    out = list(lista)
    swaps = 0
    for i in range(len(out)):
        for j in range(len(out) - 1 - i):
            if out[j] > out[j + 1]:
                out[j], out[j + 1] = out[j + 1], out[j]
                swaps += 1
    return swaps


def ordenar_por_clave(personas, clave):
    return sorted(personas, key=lambda p: p[clave])


def podio(lista):
    return sorted(lista, reverse=True)[:3]


def rango(lista):
    return max(lista) - min(lista)
