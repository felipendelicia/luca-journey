# Líder Clemont — El inventor de tests (solución de referencia).
# El preamble (doble, es_par, mayor, sumar_lista) está en meta.json y se antepone al corregir.

def probar_doble():
    assert doble(3) == 6
    assert doble(0) == 0
    assert doble(-2) == -4

def probar_es_par():
    assert es_par(2) is True
    assert es_par(3) is False
    assert es_par(0) is True
    assert es_par(7) is False

def probar_mayor():
    assert mayor(5, 3) == 5
    assert mayor(2, 8) == 8
    assert mayor(4, 4) == 4

def probar_sumar_lista():
    assert sumar_lista([1, 2, 3]) == 6
    assert sumar_lista([10, -10]) == 0
    assert sumar_lista([]) == 0
    assert sumar_lista([5]) == 5
