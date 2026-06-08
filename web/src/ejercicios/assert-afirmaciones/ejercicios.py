"""✏️ Ejercicios — assert: afirmaciones

assert verifica que algo sea verdadero; si no, lanza AssertionError. Es la base de los
TESTS y sirve para chequear supuestos en tu código. ✅ Corregir al terminar.
"""


# Afirmar que es positivo
# Verificá con assert que n sea positivo (n > 0) y devolvé n.
# Pista: assert n > 0, "n debe ser positivo".
# Ejemplo:  verificar_positivo(5)  →  5   ·   verificar_positivo(-2)  →  lanza AssertionError
def verificar_positivo(n):
    """Afirmá n > 0 y devolvé n."""
    # TU CÓDIGO ACÁ
    pass


# Afirmar el nivel
# Verificá con assert que el nivel esté entre 1 y 100, y devolvelo.
# Pista: assert 1 <= nivel <= 100.
def verificar_nivel(nivel):
    """Afirmá 1 <= nivel <= 100 y devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Promedio con assert
# Antes de calcular el promedio, verificá con assert que la lista NO esté vacía.
# Pista: assert len(numeros) > 0, "lista vacía"  →  return sum(numeros) / len(numeros).
# Ejemplo:  promedio([10, 20, 30])  →  20.0   ·   promedio([])  →  lanza AssertionError
def promedio(numeros):
    """Afirmá que la lista no esté vacía y devolvé el promedio."""
    # TU CÓDIGO ACÁ
    pass


# No negativo
# Afirmá (con assert) que n >= 0; si está bien, devolvelo. Poné un mensaje claro en el assert.
def afirmar_no_negativo(n):
    """assert n >= 0, "..."; devolvé n."""
    # TU CÓDIGO ACÁ
    pass


# En rango
# Afirmá que `lo` <= n <= `hi`; devolvé n.
def afirmar_en_rango(n, lo, hi):
    """assert lo <= n <= hi; devolvé n."""
    # TU CÓDIGO ACÁ
    pass


# No vacío
# Afirmá que el texto no es ""; devolvelo.
def afirmar_no_vacio(texto):
    """assert texto != ""; devolvé texto."""
    # TU CÓDIGO ACÁ
    pass


# Par
# Afirmá que n es par; devolvelo.
def afirmar_par(n):
    """assert n par; devolvé n."""
    # TU CÓDIGO ACÁ
    pass


# Tipo válido
# Afirmá que `tipo` está en ["Fuego", "Agua", "Planta", "Electrico"]; devolvelo.
def afirmar_tipo_valido(tipo):
    """assert tipo válido; devolvé tipo."""
    # TU CÓDIGO ACÁ
    pass


# La suma da
# Afirmá que a + b es igual a `esperado`; devolvé `esperado`.
def afirmar_suma(a, b, esperado):
    """assert a + b == esperado; devolvé esperado."""
    # TU CÓDIGO ACÁ
    pass


# Ordenada
# Afirmá que la lista está ordenada de menor a mayor; devolvela.
def afirmar_ordenada(lista):
    """assert lista ordenada; devolvé lista."""
    # TU CÓDIGO ACÁ
    pass


# Sin repetidos
# Afirmá que no hay elementos repetidos; devolvé la lista.
def afirmar_unicos(lista):
    """assert sin repetidos; devolvé lista."""
    # TU CÓDIGO ACÁ
    pass


# Misma longitud
# Afirmá que `a` y `b` tienen la misma longitud; devolvé True.
def afirmar_misma_longitud(a, b):
    """assert len(a) == len(b); devolvé True."""
    # TU CÓDIGO ACÁ
    pass


# Clave presente
# Afirmá que `clave` está en el diccionario; devolvé su valor.
def afirmar_clave(dic, clave):
    """assert clave in dic; devolvé dic[clave]."""
    # TU CÓDIGO ACÁ
    pass


# Todos positivos
# Afirmá que todos los elementos son mayores que 0; devolvé la lista.
def afirmar_positivos(lista):
    """assert todos > 0; devolvé lista."""
    # TU CÓDIGO ACÁ
    pass


# Porcentaje válido
# Afirmá que p está entre 0 y 100; devolvelo.
def afirmar_porcentaje(p):
    """assert 0 <= p <= 100; devolvé p."""
    # TU CÓDIGO ACÁ
    pass


# Es entero
# Afirmá que x es un int; devolvelo.
def afirmar_es_entero(x):
    """assert isinstance(x, int); devolvé x."""
    # TU CÓDIGO ACÁ
    pass


# a mayor que b
# Afirmá que a > b; devolvé a.
def afirmar_mayor(a, b):
    """assert a > b; devolvé a."""
    # TU CÓDIGO ACÁ
    pass


# Contiene
# Afirmá que x está en la lista; devolvé x.
def afirmar_contiene(lista, x):
    """assert x in lista; devolvé x."""
    # TU CÓDIGO ACÁ
    pass


# Longitud esperada
# Afirmá que la lista tiene exactamente `n` elementos; devolvela.
def afirmar_longitud(lista, n):
    """assert len(lista) == n; devolvé lista."""
    # TU CÓDIGO ACÁ
    pass


# No es None
# Afirmá que x no es None; devolvelo.
def afirmar_no_none(x):
    """assert x is not None; devolvé x."""
    # TU CÓDIGO ACÁ
    pass
