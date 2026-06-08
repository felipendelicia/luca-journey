"""✅ Soluciones — assert: afirmaciones"""


def verificar_positivo(n):
    assert n > 0, "n debe ser positivo"
    return n


def verificar_nivel(nivel):
    assert 1 <= nivel <= 100, "el nivel debe estar entre 1 y 100"
    return nivel


def promedio(numeros):
    assert len(numeros) > 0, "lista vacía"
    return sum(numeros) / len(numeros)


def afirmar_no_negativo(n):
    assert n >= 0, "no puede ser negativo"
    return n


def afirmar_en_rango(n, lo, hi):
    assert lo <= n <= hi, "fuera de rango"
    return n


def afirmar_no_vacio(texto):
    assert texto != "", "no puede estar vacío"
    return texto


def afirmar_par(n):
    assert n % 2 == 0, "debe ser par"
    return n


def afirmar_tipo_valido(tipo):
    assert tipo in ["Fuego", "Agua", "Planta", "Electrico"], "tipo inválido"
    return tipo


def afirmar_suma(a, b, esperado):
    assert a + b == esperado, "la suma no da el valor esperado"
    return esperado


def afirmar_ordenada(lista):
    assert lista == sorted(lista), "la lista no está ordenada"
    return lista


def afirmar_unicos(lista):
    assert len(lista) == len(set(lista)), "hay elementos repetidos"
    return lista


def afirmar_misma_longitud(a, b):
    assert len(a) == len(b), "las listas tienen distinta longitud"
    return True


def afirmar_clave(dic, clave):
    assert clave in dic, "falta la clave"
    return dic[clave]


def afirmar_positivos(lista):
    assert all(x > 0 for x in lista), "hay valores no positivos"
    return lista


def afirmar_porcentaje(p):
    assert 0 <= p <= 100, "el porcentaje debe estar entre 0 y 100"
    return p


def afirmar_es_entero(x):
    assert isinstance(x, int), "debe ser un entero"
    return x


def afirmar_mayor(a, b):
    assert a > b, "a debería ser mayor que b"
    return a


def afirmar_contiene(lista, x):
    assert x in lista, "el elemento no está en la lista"
    return x


def afirmar_longitud(lista, n):
    assert len(lista) == n, "la lista no tiene la longitud esperada"
    return lista


def afirmar_no_none(x):
    assert x is not None, "no puede ser None"
    return x
