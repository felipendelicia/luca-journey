# Líder Ramos — Afirmaciones de batalla (solución de referencia).

def verificar_positivo(n):
    assert n > 0
    return n

def verificar_lista(lista):
    assert len(lista) > 0
    return lista[0]

def calcular_promedio(valores):
    assert len(valores) > 0
    return sum(valores) / len(valores)

def resumen_equipo(niveles):
    assert len(niveles) > 0
    for n in niveles:
        assert n > 0
    return {
        "cantidad": len(niveles),
        "promedio": calcular_promedio(niveles),
        "max": max(niveles),
        "min": min(niveles),
    }
