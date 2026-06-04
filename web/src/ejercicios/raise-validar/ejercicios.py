"""
✏️ Ejercicios — Lanzar errores: raise

A veces TU código tiene que avisar que algo está mal. Para eso se LANZA un error
con raise. Así, quien te llama se entera del problema (en vez de seguir con datos malos).
"""


# 1) Si la edad es negativa, lanzá un ValueError. Si no, devolvé la edad.
def validar_edad(edad):
    """if edad < 0: raise ValueError("edad inválida")  -> sino devolvé edad."""
    # TU CÓDIGO ACÁ
    pass


# 2) El nivel tiene que estar entre 1 y 100. Si no, lanzá ValueError. Si sí, devolvelo.
def validar_nivel(nivel):
    """Lanzá ValueError si nivel < 1 o nivel > 100."""
    # TU CÓDIGO ACÁ
    pass


# 3) Dividí a/b, pero si b es 0, lanzá un ValueError("no se puede dividir por cero").
def dividir(a, b):
    """Lanzá ValueError si b == 0, sino devolvé a / b."""
    # TU CÓDIGO ACÁ
    pass


# 4) Si x no es un string, lanzá un TypeError. Si lo es, devolvelo.
def solo_texto(x):
    """if not isinstance(x, str): raise TypeError(...)."""
    # TU CÓDIGO ACÁ
    pass
