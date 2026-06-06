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
