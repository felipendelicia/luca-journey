"""🕸️ Soluciones — Dividir trabajo (hilos)"""
import math


def dividir(items, n):
    k, m = divmod(len(items), n)
    return [items[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def tamano_chunk(total, n):
    return math.ceil(total / n)


def cuantos_hilos(total, por_hilo):
    return math.ceil(total / por_hilo)


def aplanar(chunks):
    return [x for bloque in chunks for x in bloque]
