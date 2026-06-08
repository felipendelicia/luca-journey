"""🌀 Ejercicios — Corrutinas (async def)

Una corrutina es una función declarada con `async def`: no corre al llamarla, sino que
devuelve un objeto que se ejecuta "en segundo plano". Acá las reconocés y clasificás.
✅ Corregí cuando termines.
"""
import asyncio


# ¿Es una corrutina?
# Devolvé True si `fn` fue definida con `async def`, o False si es una función normal.
# (asyncio.iscoroutinefunction(fn) responde justo eso.)
# Ejemplo:  con  async def f(): ...   →  es_corrutina(f)  →  True
def es_corrutina(fn):
    """Devolvé True si fn es una función async."""


# Contar corrutinas
# `funcs` es una lista de funciones. Devolvé cuántas son corrutinas (async def).
# Ejemplo:  contar_corrutinas([async_f, normal_g, async_h])  →  2
def contar_corrutinas(funcs):
    """Devolvé cuántas funciones de la lista son async."""


# Nombres de las corrutinas
# Devolvé la lista de NOMBRES (fn.__name__) de las funciones que son corrutinas.
# Ejemplo:  nombres_corrutinas([async_descargar, normal_sumar])  →  ["descargar"]... según __name__
def nombres_corrutinas(funcs):
    """Devolvé los __name__ de las funciones async."""


# Escribir la firma
# Devolvé la línea de definición de una función. Si `asincrona` es True usá "async def",
# si no "def". Sin cuerpo, terminando en "():".
# Ejemplo:  firma("descargar", True)   →  "async def descargar():"
#           firma("sumar", False)      →  "def sumar():"
def firma(nombre, asincrona):
    """Devolvé 'async def nombre():' o 'def nombre():'."""


# Tipo de función
# Devolvé "async" si fn es una corrutina, o "normal" si no.
def tipo_de(fn):
    """Devolvé 'async' o 'normal'."""
    # TU CÓDIGO ACÁ


# Primera corrutina
# Devolvé el __name__ de la primera función async de la lista, o None si no hay ninguna.
def primera_corrutina(funcs):
    """Devolvé el nombre de la primera async, o None."""
    # TU CÓDIGO ACÁ


# Nombres de las normales
# Devolvé los __name__ de las funciones que NO son async.
def nombres_normales(funcs):
    """Devolvé los nombres de las funciones normales."""
    # TU CÓDIGO ACÁ


# Solo las corrutinas
# Devolvé una lista con las funciones async (los objetos función, no los nombres).
def solo_corrutinas(funcs):
    """Devolvé las funciones async."""
    # TU CÓDIGO ACÁ


# Firma con argumentos
# Devolvé la línea de definición. `args` es una lista de nombres de parámetros.
# Ejemplo:  firma_con_args("bajar", ["url", "destino"], True)  →  "async def bajar(url, destino):"
def firma_con_args(nombre, args, asincrona):
    """Devolvé 'def'/'async def' nombre(args):."""
    # TU CÓDIGO ACÁ


# Agregar async
# Dada una línea "def f():", devolvé "async def f():". Si ya empieza con "async ", dejala igual.
def agregar_async(linea):
    """Convertí 'def …' en 'async def …'."""
    # TU CÓDIGO ACÁ


# Quitar async
# Dada "async def f():", devolvé "def f():". Si no empieza con "async ", dejala igual.
def quitar_async(linea):
    """Convertí 'async def …' en 'def …'."""
    # TU CÓDIGO ACÁ


# ¿Es definición async?
# Devolvé True si la línea (ignorando espacios al inicio) empieza con "async def".
def es_definicion_async(linea):
    """Devolvé True si es una definición async."""
    # TU CÓDIGO ACÁ


# Nombre de la firma
# De una línea como "async def descargar():" o "def sumar():", devolvé solo el nombre.
# Ejemplo:  nombre_de_firma("async def descargar():")  →  "descargar"
def nombre_de_firma(linea):
    """Devolvé el nombre de la función de la firma."""
    # TU CÓDIGO ACÁ


# Contar awaits
# Devolvé cuántas veces aparece "await " en el código.
# Ejemplo:  cuenta_awaits("await a()\n await b()")  →  2
def cuenta_awaits(codigo):
    """Devolvé cuántos 'await ' hay en el código."""
    # TU CÓDIGO ACÁ


# ¿Tiene await?
# Devolvé True si el código contiene "await ".
def tiene_await(codigo):
    """Devolvé True si hay un await."""
    # TU CÓDIGO ACÁ


# Clasificar todas
# Devolvé un dict __name__ → "async"/"normal" para cada función de la lista.
def clasificar_todas(funcs):
    """Devolvé un dict nombre → 'async'/'normal'."""
    # TU CÓDIGO ACÁ


# ¿Hay alguna async?
# Devolvé True si al menos una función de la lista es async.
def hay_alguna_async(funcs):
    """Devolvé True si hay al menos una async."""
    # TU CÓDIGO ACÁ


# ¿Todas async?
# Devolvé True si TODAS las funciones de la lista son async.
def todas_async(funcs):
    """Devolvé True si todas son async."""
    # TU CÓDIGO ACÁ


# Proporción async
# Devolvé la fracción de funciones que son async (cantidad async / total).
# Ejemplo:  con 1 async de 4  →  proporcion_async(funcs)  →  0.25
def proporcion_async(funcs):
    """Devolvé la fracción de funciones async."""
    # TU CÓDIGO ACÁ


# Lista de firmas
# Dada una lista de nombres, devolvé una lista de firmas (todas async si `asincrona` es True).
# Ejemplo:  firma_lista(["a", "b"], True)  →  ["async def a():", "async def b():"]
def firma_lista(nombres, asincrona):
    """Devolvé las firmas de cada nombre."""
    # TU CÓDIGO ACÁ
