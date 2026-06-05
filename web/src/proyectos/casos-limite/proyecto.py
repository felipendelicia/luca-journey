# Líder Valerie — Defensora de los bordes (solución de referencia).

def primero_seguro(lista):
    if len(lista) == 0:
        return None
    return lista[0]

def maximo_seguro(lista):
    if len(lista) == 0:
        return None
    return max(lista)

def longitud_segura(valor):
    if valor is None:
        return 0
    if isinstance(valor, (list, str)):
        return len(valor)
    return 0

def nivel_promedio(equipo):
    if equipo is None:
        return 0
    niveles = [p["nivel"] for p in equipo if "nivel" in p]
    if len(niveles) == 0:
        return 0
    return sum(niveles) / len(niveles)
