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


def tipo_de(fn):
    return "async" if asyncio.iscoroutinefunction(fn) else "normal"


def primera_corrutina(funcs):
    for f in funcs:
        if asyncio.iscoroutinefunction(f):
            return f.__name__
    return None


def nombres_normales(funcs):
    return [f.__name__ for f in funcs if not asyncio.iscoroutinefunction(f)]


def solo_corrutinas(funcs):
    return [f for f in funcs if asyncio.iscoroutinefunction(f)]


def firma_con_args(nombre, args, asincrona):
    prefijo = "async def" if asincrona else "def"
    return f"{prefijo} {nombre}({', '.join(args)}):"


def agregar_async(linea):
    if linea.startswith("async "):
        return linea
    return "async " + linea


def quitar_async(linea):
    if linea.startswith("async "):
        return linea[len("async "):]
    return linea


def es_definicion_async(linea):
    return linea.strip().startswith("async def")


def nombre_de_firma(linea):
    sin = linea.replace("async def", "def").strip()
    return sin[len("def "):sin.index("(")].strip()


def cuenta_awaits(codigo):
    return codigo.count("await ")


def tiene_await(codigo):
    return "await " in codigo


def clasificar_todas(funcs):
    return {f.__name__: ("async" if asyncio.iscoroutinefunction(f) else "normal") for f in funcs}


def hay_alguna_async(funcs):
    return any(asyncio.iscoroutinefunction(f) for f in funcs)


def todas_async(funcs):
    return all(asyncio.iscoroutinefunction(f) for f in funcs)


def proporcion_async(funcs):
    n = sum(1 for f in funcs if asyncio.iscoroutinefunction(f))
    return n / len(funcs)


def firma_lista(nombres, asincrona):
    prefijo = "async def" if asincrona else "def"
    return [f"{prefijo} {n}():" for n in nombres]
