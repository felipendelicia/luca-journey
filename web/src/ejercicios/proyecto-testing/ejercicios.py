"""✏️ Ejercicios — Proyecto: módulo testeado

Junta todo Kalos: funciones ROBUSTAS (que validan y manejan errores) y sus TESTS.
Así se escribe código de calidad en el mundo real. ✅ Corregir al terminar.
"""


# Raíz robusta
# raiz_cuadrada(n): si n es negativo, lanzá ValueError. Si no, devolvé la raíz (n ** 0.5).
# Ejemplo:  raiz_cuadrada(9)  →  3.0   ·   raiz_cuadrada(-4)  →  lanza ValueError
def raiz_cuadrada(n):
    """Lanzá ValueError si n < 0; sino devolvé n ** 0.5."""
    # TU CÓDIGO ACÁ
    pass


# Test de la raíz
# Escribí un test para 'raiz' (una raíz cuadrada). Verificá: raiz(9) == 3, raiz(0) == 0,
# y que raiz(-1) LANCE ValueError. Pista: usá try/except para el caso de error.
def probar_raiz(raiz):
    """Hacé asserts e incluí que el negativo lance ValueError."""
    # TU CÓDIGO ACÁ
    pass


# División segura
# dividir_seguro(a, b): devolvé a/b, pero si b es 0 devolvé None (sin explotar).
# Pista: try/except ZeroDivisionError.
def dividir_seguro(a, b):
    """Devolvé a / b, o None si b es 0."""
    # TU CÓDIGO ACÁ
    pass


# Test de la división segura
# Escribí un test para 'dividir_seguro'. Verificá: dividir_seguro(6, 2) == 3 y
# dividir_seguro(1, 0) is None.
def probar_dividir_seguro(dividir_seguro):
    """Probá el caso normal y el caso del cero."""
    # TU CÓDIGO ACÁ
    pass


# Clasificar nivel
# Devolvé "bajo" si n < 30, "medio" si n < 70, o "alto" en otro caso.
def clasificar_nivel(n):
    """Devolvé 'bajo', 'medio' o 'alto' según n."""
    # TU CÓDIGO ACÁ
    pass


# Probar clasificar_nivel
# `f(n)` debería clasificar el nivel. Escribí asserts para los tres rangos.
def probar_clasificar_nivel(f):
    """Verificá f en los tres rangos."""
    # TU CÓDIGO ACÁ
    pass


# Iniciales
# Devolvé las iniciales (primera letra de cada palabra en mayúscula).
def iniciales(nombre):
    """Devolvé las iniciales en mayúscula."""
    # TU CÓDIGO ACÁ
    pass


# Probar iniciales
# `f(nombre)` debería devolver las iniciales.
def probar_iniciales(f):
    """Verificá f con un nombre de dos palabras."""
    # TU CÓDIGO ACÁ
    pass


# Contar mayúsculas
# Devolvé cuántas letras mayúsculas tiene el texto.
def contar_mayuscula(texto):
    """Devolvé cuántas mayúsculas hay."""
    # TU CÓDIGO ACÁ
    pass


# Probar contar_mayuscula
# `f(texto)` debería contar las mayúsculas.
def probar_contar_mayuscula(f):
    """Verificá f con un texto mezclado."""
    # TU CÓDIGO ACÁ
    pass


# ¿Es múltiplo?
# Devolvé True si n es múltiplo de m.
def es_multiplo(n, m):
    """Devolvé True si n es múltiplo de m."""
    # TU CÓDIGO ACÁ
    pass


# Probar es_multiplo
# `f(n, m)` debería decir si n es múltiplo de m.
def probar_es_multiplo(f):
    """Verificá f con un caso True y uno False."""
    # TU CÓDIGO ACÁ
    pass


# Distancia
# Devolvé la distancia (diferencia absoluta) entre a y b.
def distancia(a, b):
    """Devolvé |a - b|."""
    # TU CÓDIGO ACÁ
    pass


# Probar distancia
# `f(a, b)` debería ser la distancia. Probá en los dos órdenes (debería dar lo mismo).
def probar_distancia(f):
    """Verificá f en ambos órdenes."""
    # TU CÓDIGO ACÁ
    pass


# Juntar
# Devolvé los elementos de la lista unidos por `sep`.
# Ejemplo:  juntar(["a", "b"], "-")  →  "a-b"
def juntar(lista, sep):
    """Devolvé la lista unida por sep."""
    # TU CÓDIGO ACÁ
    pass


# Probar juntar
# `f(lista, sep)` debería unir con el separador.
def probar_juntar(f):
    """Verificá f con un separador."""
    # TU CÓDIGO ACÁ
    pass


# Limitar
# Devolvé n, pero nunca mayor que `maximo`.
def limite(n, maximo):
    """Devolvé min(n, maximo)."""
    # TU CÓDIGO ACÁ
    pass


# Probar limite
# `f(n, maximo)` debería recortar al máximo. Probá adentro y por encima.
def probar_limite(f):
    """Verificá f adentro y por encima del máximo."""
    # TU CÓDIGO ACÁ
    pass


# Repetir lista
# Devolvé la lista repetida n veces.
# Ejemplo:  repetir_lista([1, 2], 2)  →  [1, 2, 1, 2]
def repetir_lista(lista, n):
    """Devolvé la lista repetida n veces."""
    # TU CÓDIGO ACÁ
    pass


# Probar repetir_lista
# `f(lista, n)` debería repetir la lista.
def probar_repetir_lista(f):
    """Verificá f con una repetición."""
    # TU CÓDIGO ACÁ
    pass
