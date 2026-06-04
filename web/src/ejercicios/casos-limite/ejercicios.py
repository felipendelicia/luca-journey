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
