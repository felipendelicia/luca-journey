"""
✏️ Ejercicios — Proyecto: módulo testeado

Junta todo Kalos: funciones ROBUSTAS (que validan y manejan errores) y sus TESTS.
Así se escribe código de calidad en el mundo real.
"""


# 1) raiz_cuadrada(n): si n es negativo, lanzá ValueError. Si no, devolvé la raíz (n ** 0.5).
def raiz_cuadrada(n):
    """Validá: no hay raíz de números negativos."""
    # TU CÓDIGO ACÁ
    pass


# 2) Test para 'raiz' (una raíz cuadrada). Verificá: raiz(9)==3, raiz(0)==0, y que
#    raiz(-1) LANCE ValueError.
def probar_raiz(raiz):
    """Incluí el caso de error (negativo) con try/except, como en 'casos límite'."""
    # TU CÓDIGO ACÁ
    pass


# 3) dividir_seguro(a, b): devolvé a/b, pero si b es 0, devolvé None (sin explotar).
def dividir_seguro(a, b):
    """Usá try/except ZeroDivisionError."""
    # TU CÓDIGO ACÁ
    pass


# 4) Test para 'dividir_seguro'. Verificá: dividir_seguro(6,2)==3 y dividir_seguro(1,0) is None.
def probar_dividir_seguro(dividir_seguro):
    """Probá el caso normal Y el caso del cero."""
    # TU CÓDIGO ACÁ
    pass
