# Líder Olympia — Tests primero (solución de referencia).

def invertir(texto):
    return texto[::-1]

def contar_vocales(texto):
    return sum(1 for c in texto.lower() if c in "aeiou")

def es_palindromo(texto):
    t = texto.lower()
    return t == t[::-1]

def resumir(texto):
    return {
        "largo": len(texto),
        "vocales": contar_vocales(texto),
        "invertido": invertir(texto),
        "palindromo": es_palindromo(texto),
    }
