"""✅ Soluciones — Lanzar errores: raise"""


def validar_edad(edad):
    if edad < 0:
        raise ValueError("edad inválida")
    return edad


def validar_nivel(nivel):
    if nivel < 1 or nivel > 100:
        raise ValueError("el nivel debe estar entre 1 y 100")
    return nivel


def dividir(a, b):
    if b == 0:
        raise ValueError("no se puede dividir por cero")
    return a / b


def solo_texto(x):
    if not isinstance(x, str):
        raise TypeError("debe ser un string")
    return x


def validar_hp(hp):
    if hp < 0 or hp > 100:
        raise ValueError("hp fuera de rango")
    return hp


def validar_no_vacio(texto):
    if texto == "":
        raise ValueError("no puede estar vacío")
    return texto


def validar_positivo(n):
    if n <= 0:
        raise ValueError("debe ser positivo")
    return n


def validar_tipo(tipo):
    if tipo not in ["Fuego", "Agua", "Planta", "Electrico"]:
        raise ValueError("tipo inválido")
    return tipo


def raiz(n):
    if n < 0:
        raise ValueError("no hay raíz real de un negativo")
    return n ** 0.5


def retirar(saldo, monto):
    if monto > saldo:
        raise ValueError("saldo insuficiente")
    return saldo - monto


def validar_porcentaje(p):
    if p < 0 or p > 100:
        raise ValueError("porcentaje fuera de 0..100")
    return p


def validar_email(texto):
    if "@" not in texto:
        raise ValueError("email inválido")
    return texto


def indexar(lista, i):
    if i < 0 or i >= len(lista):
        raise IndexError("posición fuera de rango")
    return lista[i]


def validar_par(n):
    if n % 2 != 0:
        raise ValueError("debe ser par")
    return n


def validar_longitud(texto, minimo):
    if len(texto) < minimo:
        raise ValueError("muy corto")
    return texto


def dividir_entero(a, b):
    if b == 0:
        raise ZeroDivisionError("no se divide por cero")
    return a // b


def validar_rango(n, lo, hi):
    if n < lo or n > hi:
        raise ValueError("fuera de rango")
    return n


def validar_lista_no_vacia(lista):
    if len(lista) == 0:
        raise ValueError("lista vacía")
    return lista


def validar_clave(dic, clave):
    if clave not in dic:
        raise KeyError(clave)
    return dic[clave]


def validar_mayor_de_edad(edad):
    if edad < 18:
        raise ValueError("menor de edad")
    return edad
