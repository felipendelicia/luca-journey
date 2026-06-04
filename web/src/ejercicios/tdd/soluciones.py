"""✅ Soluciones — TDD: el test primero"""


def es_palindromo(texto):
    return texto == texto[::-1]


def factorial(n):
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def contar_vocales(texto):
    return sum(1 for letra in texto.lower() if letra in "aeiou")
