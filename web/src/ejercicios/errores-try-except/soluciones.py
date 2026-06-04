"""✅ Soluciones — Errores: try / except"""


def dividir_seguro(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


def a_entero(texto):
    try:
        return int(texto)
    except ValueError:
        return 0


def elemento(lista, i):
    try:
        return lista[i]
    except IndexError:
        return None


def valor(dic, clave):
    try:
        return dic[clave]
    except KeyError:
        return "no encontrado"
