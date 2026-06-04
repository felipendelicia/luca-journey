"""✏️ Ejercicios — Lanzar errores: raise

A veces TU código tiene que avisar que algo está mal. Para eso se LANZA un error con
raise: quien te llama se entera (en vez de seguir con datos malos). ✅ Corregir al terminar.
"""


# Validar la edad
# Si la edad es negativa, lanzá un ValueError. Si no, devolvé la edad.
# Pista: if edad < 0: raise ValueError("edad inválida").
# Ejemplo:  validar_edad(25)  →  25   ·   validar_edad(-1)  →  lanza ValueError
def validar_edad(edad):
    """Lanzá ValueError si edad < 0; sino devolvé edad."""
    # TU CÓDIGO ACÁ
    pass


# Validar el nivel
# El nivel tiene que estar entre 1 y 100. Si no, lanzá ValueError. Si sí, devolvelo.
# Ejemplo:  validar_nivel(50)  →  50   ·   validar_nivel(0)  →  lanza ValueError
def validar_nivel(nivel):
    """Lanzá ValueError si nivel < 1 o > 100; sino devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Dividir con aviso
# Dividí a/b, pero si b es 0 lanzá ValueError("no se puede dividir por cero").
# Ejemplo:  dividir(10, 2)  →  5.0   ·   dividir(5, 0)  →  lanza ValueError
def dividir(a, b):
    """Lanzá ValueError si b == 0; sino devolvé a / b."""
    # TU CÓDIGO ACÁ
    pass


# Solo texto
# Si x NO es un string, lanzá un TypeError. Si lo es, devolvelo.
# Pista: if not isinstance(x, str): raise TypeError(...).
# Ejemplo:  solo_texto("Pikachu")  →  "Pikachu"   ·   solo_texto(123)  →  lanza TypeError
def solo_texto(x):
    """Lanzá TypeError si x no es str; sino devolvelo."""
    # TU CÓDIGO ACÁ
    pass
