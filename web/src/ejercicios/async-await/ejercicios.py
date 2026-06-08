"""⏳ Ejercicios — await: dónde esperar

`await` se pone delante de las operaciones que ESPERAN (bajar algo, leer una API):
mientras esperan, el programa hace otra cosa. Acá decidís qué pasos lo necesitan.
Modelamos cada paso como un dict {"nombre", "espera": bool}. ✅ Corregí cuando termines.
"""


# ¿Este paso necesita await?
# Devolvé True si el paso es una operación que espera (su clave "espera" es True).
# Ejemplo:  necesita_await({"nombre": "bajar", "espera": True})  →  True
def necesita_await(paso):
    """Devolvé el valor de paso['espera']."""


# Pasos que llevan await
# `pasos` es una lista de esos dicts. Devolvé los NOMBRES de los que esperan.
# Ejemplo:  pasos_con_await([{"nombre":"bajar","espera":True},{"nombre":"sumar","espera":False}])
#               →  ["bajar"]
def pasos_con_await(pasos):
    """Devolvé los nombres de los pasos que esperan."""


# Agregar await a una línea
# Devolvé la línea con "await " adelante. Si YA empieza con "await ", devolvela igual.
# Ejemplo:  agregar_await("bajar(url)")        →  "await bajar(url)"
#           agregar_await("await bajar(url)")  →  "await bajar(url)"
def agregar_await(linea):
    """Devolvé la línea con 'await ' adelante (sin duplicar)."""


# Contar awaits
# Devolvé cuántas veces aparece "await " en un bloque de código (texto).
# Ejemplo:  contar_awaits("a = await f()\nb = await g()")  →  2
def contar_awaits(codigo):
    """Devolvé cuántos 'await ' hay en el código."""


# Quitar await
# Si la línea empieza con "await ", quitáselo y devolvé el resto. Si no, devolvela igual.
# Ejemplo:  quitar_await("await bajar()")  →  "bajar()"
def quitar_await(linea):
    """Sacá el 'await ' del inicio si está."""
    # TU CÓDIGO ACÁ


# ¿Tiene await?
# Devolvé True si la línea empieza con "await ".
def tiene_await_linea(linea):
    """Devolvé True si la línea empieza con await."""
    # TU CÓDIGO ACÁ


# Líneas con await
# Devolvé las líneas que empiezan con "await ".
def lineas_con_await(lineas):
    """Devolvé las líneas que tienen await."""
    # TU CÓDIGO ACÁ


# Líneas sin await
# Devolvé las líneas que NO empiezan con "await ".
def lineas_sin_await(lineas):
    """Devolvé las líneas sin await."""
    # TU CÓDIGO ACÁ


# Índices con await
# Devolvé los índices de las líneas que empiezan con "await ".
# Ejemplo:  indices_con_await(["x=1", "await a()", "await b()"])  →  [1, 2]
def indices_con_await(lineas):
    """Devolvé los índices de las líneas con await."""
    # TU CÓDIGO ACÁ


# Cuántas con await
# Devolvé cuántas líneas empiezan con "await ".
def cuantas_con_await(lineas):
    """Devolvé cuántas líneas tienen await."""
    # TU CÓDIGO ACÁ


# ¿Todas con await?
# Devolvé True si TODAS las líneas empiezan con "await ".
def todas_con_await(lineas):
    """Devolvé True si todas tienen await."""
    # TU CÓDIGO ACÁ


# ¿Ninguna con await?
# Devolvé True si NINGUNA línea empieza con "await ".
def ninguna_con_await(lineas):
    """Devolvé True si ninguna tiene await."""
    # TU CÓDIGO ACÁ


# Agregar await a todas
# Devolvé las líneas con "await " adelante (las que ya lo tienen quedan igual).
def agregar_await_a_todas(lineas):
    """Agregá await a las líneas que no lo tienen."""
    # TU CÓDIGO ACÁ


# Quitar await de todas
# Devolvé las líneas sin el "await " del inicio.
def quitar_await_de_todas(lineas):
    """Sacá el await de todas las líneas."""
    # TU CÓDIGO ACÁ


# Primer índice con await
# Devolvé el índice de la primera línea con "await ", o -1 si no hay ninguna.
def primer_indice_await(lineas):
    """Devolvé el primer índice con await, o -1."""
    # TU CÓDIGO ACÁ


# Proporción con await
# Devolvé la fracción de líneas que tienen await (cantidad con await / total).
def proporcion_con_await(lineas):
    """Devolvé la fracción de líneas con await."""
    # TU CÓDIGO ACÁ


# Normalizar await
# Si la línea tiene varios "await " repetidos al inicio, dejá uno solo. Si no tiene, agregá uno.
# Ejemplo:  normalizar_await("await await f()")  →  "await f()"   ·   normalizar_await("f()")  →  "await f()"
def normalizar_await(linea):
    """Dejá exactamente un await al inicio."""
    # TU CÓDIGO ACÁ


# Contar awaits en el código
# Devolvé cuántas veces aparece "await " en todo el texto (puede tener varias líneas).
def contar_await_total(codigo):
    """Devolvé cuántos 'await ' hay en el código."""
    # TU CÓDIGO ACÁ


# La más corta con await
# Devolvé la línea con await más corta, o None si no hay ninguna.
def mas_corta_con_await(lineas):
    """Devolvé la línea con await más corta, o None."""
    # TU CÓDIGO ACÁ


# Juntar líneas
# Devolvé todas las líneas unidas con un salto de línea (\n).
def juntar_lineas(lineas):
    """Devolvé las líneas unidas por '\\n'."""
    # TU CÓDIGO ACÁ
