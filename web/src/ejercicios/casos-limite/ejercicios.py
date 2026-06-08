"""✏️ Ejercicios — Casos límite y errores

Un buen test no prueba solo "lo fácil": prueba los CASOS LÍMITE (lista vacía, cero, el
mínimo) y que la función LANCE el error correcto cuando debe. ✅ Corregir al terminar.
"""


# Probar el caso vacío
# Test para 'largo' (largo de un texto). Probá un caso normal Y el caso LÍMITE del texto
# vacío: largo("hola") == 4, largo("") == 0, largo("a") == 1. (El vacío esconde bugs.)
def probar_largo(largo):
    """Hacé asserts sobre largo(...), incluyendo el texto vacío."""
    # TU CÓDIGO ACÁ
    pass


# Probar suma con vacía
# Test para 'suma_lista'. Probá: suma_lista([1, 2, 3]) == 6, suma_lista([]) == 0 (vacía),
# suma_lista([7]) == 7.
def probar_suma_lista(suma_lista):
    """Hacé asserts incluyendo el caso de la lista vacía."""
    # TU CÓDIGO ACÁ
    pass


# Probar que lance error
# Test para 'dividir'. Verificá que dividir(10, 2) == 5 Y que dividir(x, 0) LANCE
# ZeroDivisionError. Si no lanza, tu test debe fallar con AssertionError.
# Pista: usá try/except ZeroDivisionError; si NO lanzó, hacé raise AssertionError(...).
def probar_dividir(dividir):
    """Verificá el caso normal y que el cero lance ZeroDivisionError."""
    # TU CÓDIGO ACÁ
    pass


# Probar división segura
# `div(a, b)` devuelve a/b, o None si b es 0. Probá el caso normal Y el caso límite (b=0).
def probar_division_segura(div):
    """Verificá div, incluyendo dividir por cero."""
    # TU CÓDIGO ACÁ
    pass


# Probar primero seguro
# `primero(lista)` devuelve el primer elemento, o None si está vacía. Probá ambos casos.
def probar_primero_seguro(primero):
    """Verificá primero, incluyendo la lista vacía."""
    # TU CÓDIGO ACÁ
    pass


# Probar último seguro
# `ultimo(lista)` devuelve el último, o None si está vacía.
def probar_ultimo_seguro(ultimo):
    """Verificá ultimo, incluyendo la lista vacía."""
    # TU CÓDIGO ACÁ
    pass


# Probar promedio seguro
# `promedio(lista)` devuelve el promedio, o 0 si está vacía.
def probar_promedio_seguro(promedio):
    """Verificá promedio, incluyendo la lista vacía."""
    # TU CÓDIGO ACÁ
    pass


# Probar máximo seguro
# `maximo(lista)` devuelve el mayor, o None si está vacía.
def probar_maximo_seguro(maximo):
    """Verificá maximo, incluyendo la lista vacía."""
    # TU CÓDIGO ACÁ
    pass


# Probar es_vacio
# `es_vacio(lista)` devuelve True si la lista está vacía.
def probar_es_vacio(es_vacio):
    """Verificá es_vacio con una lista vacía y una con elementos."""
    # TU CÓDIGO ACÁ
    pass


# Probar clamp
# `clamp(n, lo, hi)` devuelve n recortado al rango [lo, hi]. Probá adentro Y en ambos bordes.
def probar_clamp(clamp):
    """Verificá clamp adentro y en los dos bordes."""
    # TU CÓDIGO ACÁ
    pass


# Probar signo
# `signo(n)` devuelve -1, 0 o 1. Probá el caso límite n=0.
def probar_signo(signo):
    """Verificá signo, incluyendo n=0."""
    # TU CÓDIGO ACÁ
    pass


# Probar porcentaje
# `porcentaje(parte, total)` devuelve parte/total*100, o 0 si total es 0.
def probar_porcentaje(porcentaje):
    """Verificá porcentaje, incluyendo total=0."""
    # TU CÓDIGO ACÁ
    pass


# Probar índice seguro
# `en(lista, i)` devuelve lista[i], o None si i está fuera de rango.
def probar_indice_seguro(en):
    """Verificá en, incluyendo un índice fuera de rango."""
    # TU CÓDIGO ACÁ
    pass


# Probar contar vocales
# `contar(texto)` cuenta las vocales. Probá un texto sin vocales (caso límite 0).
def probar_contar_vocales(contar):
    """Verificá contar, incluyendo un texto sin vocales."""
    # TU CÓDIGO ACÁ
    pass


# Probar recortar
# `recortar(texto, n)` devuelve los primeros n caracteres. Probá cuando n es mayor que el largo.
def probar_recortar(recortar):
    """Verificá recortar, incluyendo n mayor que el largo."""
    # TU CÓDIGO ACÁ
    pass


# Probar quitar negativos
# `quitar(lista)` devuelve solo los elementos >= 0. Probá una lista toda negativa (caso límite []).
def probar_quitar_negativos(quitar):
    """Verificá quitar, incluyendo una lista toda negativa."""
    # TU CÓDIGO ACÁ
    pass


# Probar primera palabra
# `primera(texto)` devuelve la primera palabra, o "" si no hay.
def probar_primera_palabra(primera):
    """Verificá primera, incluyendo el texto vacío."""
    # TU CÓDIGO ACÁ
    pass


# Probar mínimo seguro
# `minimo(lista)` devuelve el menor, o None si está vacía.
def probar_minimo_seguro(minimo):
    """Verificá minimo, incluyendo la lista vacía."""
    # TU CÓDIGO ACÁ
    pass


# Probar dividir lista
# `dividir(lista, d)` divide cada elemento por d, o None si d es 0.
def probar_dividir_lista(dividir):
    """Verificá dividir, incluyendo d=0."""
    # TU CÓDIGO ACÁ
    pass


# Probar es_positivo
# `es_positivo(n)` devuelve True solo si n > 0. Probá el caso límite n=0.
def probar_es_positivo(es_positivo):
    """Verificá es_positivo, incluyendo n=0."""
    # TU CÓDIGO ACÁ
    pass
