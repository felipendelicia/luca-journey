"""🪢 Soluciones — Juntar resultados (gather)"""


def combinar(resultados):
    return {nombre: valor for nombre, valor in resultados}


def en_orden(nombres, valores):
    return {n: v for n, v in zip(nombres, valores)}


def todos_ok(resultados):
    return all(r is not None for r in resultados)


def primer_error(resultados):
    for i, r in enumerate(resultados):
        if r is None:
            return i
    return -1
