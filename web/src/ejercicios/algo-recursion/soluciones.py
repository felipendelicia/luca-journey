"""🔁 Soluciones — Recursión"""


def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


def suma_hasta(n):
    if n == 0:
        return 0
    return n + suma_hasta(n - 1)


def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def potencia(base, exp):
    if exp == 0:
        return 1
    return base * potencia(base, exp - 1)


def cuenta_regresiva(n):
    if n <= 0:
        return "Ya!"
    return str(n) + "," + cuenta_regresiva(n - 1)


def suma_lista(lista):
    if not lista:
        return 0
    return lista[0] + suma_lista(lista[1:])


def largo(lista):
    if not lista:
        return 0
    return 1 + largo(lista[1:])


def maximo(lista):
    if len(lista) == 1:
        return lista[0]
    resto = maximo(lista[1:])
    return lista[0] if lista[0] > resto else resto


def invertir_texto(texto):
    if texto == "":
        return ""
    return invertir_texto(texto[1:]) + texto[0]


def es_palindromo(texto):
    if len(texto) <= 1:
        return True
    if texto[0] != texto[-1]:
        return False
    return es_palindromo(texto[1:-1])


def contar_apariciones(lista, x):
    if not lista:
        return 0
    return (1 if lista[0] == x else 0) + contar_apariciones(lista[1:], x)


def multiplicar(a, b):
    if b == 0:
        return 0
    return a + multiplicar(a, b - 1)


def mcd(a, b):
    if b == 0:
        return a
    return mcd(b, a % b)


def suma_digitos(n):
    if n < 10:
        return n
    return n % 10 + suma_digitos(n // 10)


def aplanar(lista):
    out = []
    for e in lista:
        if isinstance(e, list):
            out.extend(aplanar(e))
        else:
            out.append(e)
    return out


def binomial(n, k):
    if k == 0 or k == n:
        return 1
    return binomial(n - 1, k - 1) + binomial(n - 1, k)


def hanoi_movimientos(n):
    if n == 0:
        return 0
    return 2 * hanoi_movimientos(n - 1) + 1


def busqueda_binaria_rec(ordenada, x):
    def buscar(lo, hi):
        if lo > hi:
            return -1
        mid = (lo + hi) // 2
        if ordenada[mid] == x:
            return mid
        if ordenada[mid] < x:
            return buscar(mid + 1, hi)
        return buscar(lo, mid - 1)
    return buscar(0, len(ordenada) - 1)


def contar_pares(lista):
    if not lista:
        return 0
    return (1 if lista[0] % 2 == 0 else 0) + contar_pares(lista[1:])


def cantidad_digitos(n):
    if n < 10:
        return 1
    return 1 + cantidad_digitos(n // 10)
