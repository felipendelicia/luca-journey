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


def raiz_segura(n):
    import math
    try:
        return math.sqrt(n)
    except ValueError:
        return None


def promedio_seguro(lista):
    try:
        return sum(lista) / len(lista)
    except ZeroDivisionError:
        return 0


def primer_elemento(lista):
    try:
        return lista[0]
    except IndexError:
        return None


def a_float_seguro(texto):
    try:
        return float(texto)
    except ValueError:
        return None


def dividir_lista(numeros, divisor):
    try:
        return [n / divisor for n in numeros]
    except ZeroDivisionError:
        return None


def buscar_indice(lista, x):
    try:
        return lista.index(x)
    except ValueError:
        return -1


def convertir_todos(textos):
    out = []
    for t in textos:
        try:
            out.append(int(t))
        except ValueError:
            out.append(0)
    return out


def acceso_anidado(dic, claves):
    actual = dic
    try:
        for k in claves:
            actual = actual[k]
        return actual
    except (KeyError, TypeError, IndexError):
        return None


def dividir_o_mensaje(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "no se puede dividir por cero"


def sumar_validos(textos):
    total = 0
    for t in textos:
        try:
            total += int(t)
        except ValueError:
            pass
    return total


def max_seguro(lista):
    try:
        return max(lista)
    except ValueError:
        return None


def leer_o_cero(dic, clave):
    try:
        return dic[clave]
    except KeyError:
        return 0


def ejecutar_seguro(func, x):
    try:
        return func(x)
    except Exception:
        return None


def cuantos_validos(textos):
    n = 0
    for t in textos:
        try:
            int(t)
            n += 1
        except ValueError:
            pass
    return n


def ultimo_elemento(lista):
    try:
        return lista[-1]
    except IndexError:
        return None


def a_entero_o(texto, default):
    try:
        return int(texto)
    except ValueError:
        return default
