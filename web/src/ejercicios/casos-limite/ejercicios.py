"""
✏️ Ejercicios — Casos límite y errores

Un buen test no prueba solo "lo fácil": prueba los CASOS LÍMITE (lista vacía, cero,
el mínimo) y que la función LANCE el error correcto cuando debe.
"""


# 1) Test para 'largo' (largo de un texto). Probá un caso normal Y el caso LÍMITE
#    del texto vacío: largo("hola")==4, largo("")==0, largo("a")==1.
def probar_largo(largo):
    """Asegurate de incluir el caso vacío (el que más bugs esconde)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Test para 'suma_lista'. Probá: suma([1,2,3])==6, suma([])==0 (vacía), suma([7])==7.
def probar_suma_lista(suma_lista):
    """Incluí el caso de la lista vacía."""
    # TU CÓDIGO ACÁ
    pass


# 3) Test para 'dividir'. Verificá que dividir(10,2)==5 Y que dividir(x, 0) LANCE
#    ZeroDivisionError. Si no lanza, tu test debe fallar con AssertionError.
def probar_dividir(dividir):
    """Pista: usá try/except ZeroDivisionError; si NO lanzó, hacé raise AssertionError(...)."""
    # TU CÓDIGO ACÁ
    pass
