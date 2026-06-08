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


def lugares_libres(activos, maximo):
    return maximo - len(activos)


def esta_al_limite(activos, maximo):
    return len(activos) >= maximo


def hay_lugar(activos, maximo):
    return len(activos) < maximo


def agregar_si_cabe(activos, item, maximo):
    if len(activos) < maximo:
        activos.append(item)
    return activos


def liberar(activos, item):
    if item in activos:
        activos.remove(item)
    return activos


def tomar_hasta(pendientes, maximo):
    return pendientes[:maximo]


def resto_despues_de(pendientes, maximo):
    return pendientes[maximo:]


def cantidad_ultimo_lote(total, tam):
    r = total % tam
    if r != 0:
        return r
    return tam if total > 0 else 0


def procesar_en_lotes(items, tam, func):
    out = []
    for i in range(0, len(items), tam):
        for x in items[i:i + tam]:
            out.append(func(x))
    return out


def rondas_necesarias(total, maximo):
    return (total + maximo - 1) // maximo


def cabe_todo(total, maximo):
    return total <= maximo


def ocupacion(activos, maximo):
    return len(activos) / maximo


def limitar_lista(items, maximo):
    return items[:maximo]


def sobran(items, maximo):
    return items[maximo:]


def puede_agregar_n(activos, n, maximo):
    return len(activos) + n <= maximo


def cuantos_esperan(total, maximo):
    return max(0, total - maximo)
