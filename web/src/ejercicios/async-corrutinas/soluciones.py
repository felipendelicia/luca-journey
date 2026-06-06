"""🌀 Soluciones — Corrutinas (async def)"""
import asyncio


def es_corrutina(fn):
    return asyncio.iscoroutinefunction(fn)


def contar_corrutinas(funcs):
    return sum(1 for f in funcs if asyncio.iscoroutinefunction(f))


def nombres_corrutinas(funcs):
    return [f.__name__ for f in funcs if asyncio.iscoroutinefunction(f)]


def firma(nombre, asincrona):
    prefijo = "async def" if asincrona else "def"
    return f"{prefijo} {nombre}():"
