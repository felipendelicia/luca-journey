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
