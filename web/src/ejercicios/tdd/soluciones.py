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


def contar_palabras(texto):
    return len(texto.split())


def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)


def capitalizar(texto):
    return texto.capitalize()


def suma_pares(lista):
    return sum(x for x in lista if x % 2 == 0)


def es_bisiesto(anio):
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)


def contar_letra(texto, letra):
    return texto.count(letra)


def quitar_vocales(texto):
    return "".join(c for c in texto if c.lower() not in "aeiou")


def promedio(numeros):
    return sum(numeros) / len(numeros)


def repetir_cada(lista):
    out = []
    for x in lista:
        out.append(x)
        out.append(x)
    return out


def iniciales(nombre):
    return "".join(p[0].upper() for p in nombre.split())


def mas_largo(palabras):
    return max(palabras, key=len)


def son_anagramas(a, b):
    return sorted(a) == sorted(b)


def titulo(frase):
    return " ".join(p.capitalize() for p in frase.split())


def contar_mayusculas(texto):
    return sum(1 for c in texto if c.isupper())


def sin_repetidos(lista):
    vistos = set()
    out = []
    for x in lista:
        if x not in vistos:
            vistos.add(x)
            out.append(x)
    return out


def es_creciente(lista):
    for i in range(1, len(lista)):
        if lista[i] <= lista[i - 1]:
            return False
    return True
