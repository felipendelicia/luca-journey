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


def cuantos_ok(resultados):
    return sum(1 for r in resultados if r is not None)


def cuantos_error(resultados):
    return sum(1 for r in resultados if r is None)


def solo_ok(resultados):
    return [r for r in resultados if r is not None]


def emparejar(nombres, valores):
    return {n: v for n, v in zip(nombres, valores)}


def primer_ok(resultados):
    for r in resultados:
        if r is not None:
            return r
    return None


def ultimo_ok(resultados):
    ult = None
    for r in resultados:
        if r is not None:
            ult = r
    return ult


def reemplazar_errores(resultados, default):
    return [default if r is None else r for r in resultados]


def hay_error(resultados):
    return any(r is None for r in resultados)


def indice_primer_error(resultados):
    for i, r in enumerate(resultados):
        if r is None:
            return i
    return -1


def suma_ok(resultados):
    return sum(r for r in resultados if r is not None)


def promedio_ok(resultados):
    oks = [r for r in resultados if r is not None]
    return sum(oks) / len(oks) if oks else 0


def ordenar_ok(resultados):
    return sorted(r for r in resultados if r is not None)


def max_ok(resultados):
    oks = [r for r in resultados if r is not None]
    return max(oks) if oks else None


def todos_fallaron(resultados):
    return all(r is None for r in resultados)


def con_indice(resultados):
    return [(i, r) for i, r in enumerate(resultados)]


def contar_valores(resultados):
    from collections import Counter
    return dict(Counter(r for r in resultados if r is not None))
