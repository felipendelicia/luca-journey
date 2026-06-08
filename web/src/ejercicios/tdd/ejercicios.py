"""✏️ Ejercicios — TDD: el test primero

TDD (Test-Driven Development) = primero el TEST de lo que debe hacer la función, después
la función para que el test pase. Acá los tests ya están escritos: tu trabajo es escribir
el código que los ponga en verde 🟢. ✅ Corregir al terminar.
"""


# Palíndromo (que el test pase)
# El test dice: es_palindromo("oso") es True, es_palindromo("gato") es False,
# es_palindromo("ana") es True. Escribí la función. Pista: texto == texto[::-1].
def es_palindromo(texto):
    """Devolvé True si el texto se lee igual al derecho y al revés."""
    # TU CÓDIGO ACÁ
    pass


# Factorial (que el test pase)
# El test dice: factorial(0) == 1, factorial(1) == 1, factorial(5) == 120. Escribilo.
def factorial(n):
    """Devolvé n! (1 × 2 × ... × n; factorial(0) es 1)."""
    # TU CÓDIGO ACÁ
    pass


# Contar vocales (que el test pase)
# El test dice: contar_vocales("pikachu") == 3, contar_vocales("xyz") == 0. Escribilo.
def contar_vocales(texto):
    """Contá cuántas vocales (a, e, i, o, u) hay en el texto."""
    # TU CÓDIGO ACÁ
    pass


# Contar palabras
# Devolvé cuántas palabras tiene el texto (separadas por espacios).
# Ejemplo:  contar_palabras("atrapalos a todos")  →  3
def contar_palabras(texto):
    """Devolvé la cantidad de palabras."""
    # TU CÓDIGO ACÁ
    pass


# ¿Es primo?
# Devolvé True si n es primo (solo divisible por 1 y por sí mismo, y n >= 2).
# Ejemplo:  es_primo(7)  →  True   ·   es_primo(8)  →  False
def es_primo(n):
    """Devolvé True si n es primo."""
    # TU CÓDIGO ACÁ
    pass


# FizzBuzz
# Devolvé "Fizz" si n es múltiplo de 3, "Buzz" si de 5, "FizzBuzz" si de ambos, o el número
# como texto si de ninguno.  Ejemplo:  fizzbuzz(15)  →  "FizzBuzz"   ·   fizzbuzz(7)  →  "7"
def fizzbuzz(n):
    """Devolvé Fizz/Buzz/FizzBuzz o el número como texto."""
    # TU CÓDIGO ACÁ
    pass


# Capitalizar
# Devolvé el texto con la primera letra en mayúscula y el resto en minúscula.
# Ejemplo:  capitalizar("pIKAchu")  →  "Pikachu"
def capitalizar(texto):
    """Devolvé el texto capitalizado."""
    # TU CÓDIGO ACÁ
    pass


# Suma de pares
# Devolvé la suma de los números pares de la lista.
# Ejemplo:  suma_pares([1, 2, 3, 4])  →  6
def suma_pares(lista):
    """Devolvé la suma de los pares."""
    # TU CÓDIGO ACÁ
    pass


# ¿Año bisiesto?
# Devolvé True si el año es bisiesto (divisible por 4, salvo los de fin de siglo que no son
# divisibles por 400).  Ejemplo:  es_bisiesto(2024)  →  True   ·   es_bisiesto(1900)  →  False
def es_bisiesto(anio):
    """Devolvé True si el año es bisiesto."""
    # TU CÓDIGO ACÁ
    pass


# Contar una letra
# Devolvé cuántas veces aparece `letra` en el texto.
# Ejemplo:  contar_letra("pikachu", "a")  →  1
def contar_letra(texto, letra):
    """Devolvé cuántas veces está la letra."""
    # TU CÓDIGO ACÁ
    pass


# Quitar vocales
# Devolvé el texto sin sus vocales (a, e, i, o, u, mayúsculas o minúsculas).
# Ejemplo:  quitar_vocales("Pikachu")  →  "Pkch"
def quitar_vocales(texto):
    """Devolvé el texto sin vocales."""
    # TU CÓDIGO ACÁ
    pass


# Promedio
# Devolvé el promedio de la lista de números.
# Ejemplo:  promedio([2, 4, 6])  →  4.0
def promedio(numeros):
    """Devolvé el promedio."""
    # TU CÓDIGO ACÁ
    pass


# Repetir cada uno
# Devolvé una lista con cada elemento repetido dos veces seguidas.
# Ejemplo:  repetir_cada([1, 2])  →  [1, 1, 2, 2]
def repetir_cada(lista):
    """Devolvé cada elemento dos veces."""
    # TU CÓDIGO ACÁ
    pass


# Iniciales
# Devolvé las iniciales (primera letra de cada palabra, en mayúscula).
# Ejemplo:  iniciales("ash ketchum")  →  "AK"
def iniciales(nombre):
    """Devolvé las iniciales en mayúscula."""
    # TU CÓDIGO ACÁ
    pass


# La más larga
# Devolvé la palabra más larga de la lista (la primera si hay empate).
# Ejemplo:  mas_largo(["pi", "onix", "eevee"])  →  "eevee"
def mas_largo(palabras):
    """Devolvé la palabra más larga."""
    # TU CÓDIGO ACÁ
    pass


# ¿Anagramas?
# Devolvé True si `a` y `b` tienen las mismas letras.
# Ejemplo:  son_anagramas("roma", "amor")  →  True
def son_anagramas(a, b):
    """Devolvé True si son anagramas."""
    # TU CÓDIGO ACÁ
    pass


# Formato título
# Devolvé la frase con la primera letra de cada palabra en mayúscula.
# Ejemplo:  titulo("ciudad de plateada")  →  "Ciudad De Plateada"
def titulo(frase):
    """Devolvé la frase en formato título."""
    # TU CÓDIGO ACÁ
    pass


# Contar mayúsculas
# Devolvé cuántas letras mayúsculas tiene el texto.
# Ejemplo:  contar_mayusculas("PiKaChU")  →  4
def contar_mayusculas(texto):
    """Devolvé cuántas mayúsculas hay."""
    # TU CÓDIGO ACÁ
    pass


# Sin repetidos
# Devolvé los elementos sin repetir, en orden de aparición.
# Ejemplo:  sin_repetidos([1, 2, 1, 3, 2])  →  [1, 2, 3]
def sin_repetidos(lista):
    """Devolvé la lista sin repetidos, en orden."""
    # TU CÓDIGO ACÁ
    pass


# ¿Estrictamente creciente?
# Devolvé True si cada elemento es MAYOR que el anterior.
# Ejemplo:  es_creciente([1, 2, 3])  →  True   ·   es_creciente([1, 1, 2])  →  False
def es_creciente(lista):
    """Devolvé True si la lista es estrictamente creciente."""
    # TU CÓDIGO ACÁ
    pass
