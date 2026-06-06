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
