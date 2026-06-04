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
