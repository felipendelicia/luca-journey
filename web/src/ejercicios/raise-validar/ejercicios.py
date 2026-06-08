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


# Validar HP
# El HP va de 0 a 100. Si está fuera, lanzá ValueError. Si está bien, devolvelo.
def validar_hp(hp):
    """Lanzá ValueError si hp no está entre 0 y 100; sino devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# No vacío
# Si el texto está vacío (""), lanzá ValueError. Si no, devolvelo.
def validar_no_vacio(texto):
    """Lanzá ValueError si el texto está vacío; sino devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Positivo
# Si n no es mayor que 0, lanzá ValueError. Si sí, devolvelo.
def validar_positivo(n):
    """Lanzá ValueError si n <= 0; sino devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Tipo válido
# El tipo tiene que ser uno de "Fuego", "Agua", "Planta", "Electrico". Si no, lanzá ValueError.
def validar_tipo(tipo):
    """Lanzá ValueError si el tipo no es válido; sino devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Raíz
# Si n es negativo, lanzá ValueError (no hay raíz real). Si no, devolvé su raíz cuadrada.
def raiz(n):
    """Lanzá ValueError si n < 0; sino devolvé la raíz."""
    # TU CÓDIGO ACÁ
    pass


# Retirar dinero
# Si `monto` es mayor que `saldo`, lanzá ValueError. Si no, devolvé el saldo restante.
# Ejemplo:  retirar(100, 30)  →  70
def retirar(saldo, monto):
    """Lanzá ValueError si monto > saldo; sino devolvé saldo - monto."""
    # TU CÓDIGO ACÁ
    pass


# Porcentaje
# Debe estar entre 0 y 100. Si no, lanzá ValueError; si sí, devolvelo.
def validar_porcentaje(p):
    """Lanzá ValueError si p no está entre 0 y 100; sino devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Email
# Si el texto no tiene un "@", lanzá ValueError. Si sí, devolvelo.
def validar_email(texto):
    """Lanzá ValueError si no hay '@'; sino devolvé el texto."""
    # TU CÓDIGO ACÁ
    pass


# Indexar seguro
# Si `i` está fuera de la lista, lanzá IndexError. Si no, devolvé lista[i].
def indexar(lista, i):
    """Lanzá IndexError si i está fuera de rango; sino devolvé lista[i]."""
    # TU CÓDIGO ACÁ
    pass


# Validar par
# Si n es impar, lanzá ValueError. Si es par, devolvelo.
def validar_par(n):
    """Lanzá ValueError si n es impar; sino devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Longitud mínima
# Si el texto es más corto que `minimo`, lanzá ValueError. Si no, devolvelo.
def validar_longitud(texto, minimo):
    """Lanzá ValueError si len(texto) < minimo; sino devolvé el texto."""
    # TU CÓDIGO ACÁ
    pass


# División entera segura
# Si b es 0, lanzá ZeroDivisionError. Si no, devolvé a // b.
def dividir_entero(a, b):
    """Lanzá ZeroDivisionError si b es 0; sino devolvé a // b."""
    # TU CÓDIGO ACÁ
    pass


# Rango
# Si n no está entre `lo` y `hi` (incluidos), lanzá ValueError. Si está, devolvelo.
def validar_rango(n, lo, hi):
    """Lanzá ValueError si n no está entre lo y hi; sino devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Lista no vacía
# Si la lista está vacía, lanzá ValueError. Si no, devolvela.
def validar_lista_no_vacia(lista):
    """Lanzá ValueError si la lista está vacía; sino devolvela."""
    # TU CÓDIGO ACÁ
    pass


# Clave obligatoria
# Si `clave` no está en el diccionario, lanzá KeyError. Si está, devolvé su valor.
def validar_clave(dic, clave):
    """Lanzá KeyError si falta la clave; sino devolvé su valor."""
    # TU CÓDIGO ACÁ
    pass


# Mayor de edad
# Si la edad es menor a 18, lanzá ValueError. Si no, devolvela.
def validar_mayor_de_edad(edad):
    """Lanzá ValueError si edad < 18; sino devolvela."""
    # TU CÓDIGO ACÁ
    pass
