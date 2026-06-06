"""🚦 Soluciones — Límite de concurrencia"""
import math


def por_lotes(items, tam):
    return [items[i:i + tam] for i in range(0, len(items), tam)]


def cantidad_lotes(total, tam):
    return math.ceil(total / tam)


def cabe(activos, maximo):
    return activos < maximo


def limitar(pedidos, maximo):
    return pedidos[:maximo]
