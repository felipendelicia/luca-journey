"""🔑 Soluciones — Variables de entorno y config"""
import os


def parsear_env(texto):
    config = {}
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        config[clave.strip()] = valor.strip()
    return config


def obtener(config, clave, defecto):
    return config.get(clave, defecto)


def es_verdadero(valor):
    return valor.lower() in ("1", "true", "si", "yes")


def leer_entorno(clave, defecto):
    return os.environ.get(clave, defecto)


def claves(config):
    return list(config.keys())


def valores(config):
    return list(config.values())


def tiene_clave(config, clave):
    return clave in config


def cantidad(config):
    return len(config)


def serializar(config):
    return "\n".join(f"{k}={v}" for k, v in config.items())


def fusionar(base, extra):
    r = dict(base)
    r.update(extra)
    return r


def solo_con_prefijo(config, prefijo):
    return {k: v for k, v in config.items() if k.startswith(prefijo)}


def a_entero(config, clave, defecto):
    try:
        return int(config[clave])
    except (KeyError, ValueError):
        return defecto


def requerir(config, clave):
    if clave not in config:
        raise KeyError(clave)
    return config[clave]


def quitar_comillas(valor):
    if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
        return valor[1:-1]
    return valor


def es_comentario(linea):
    return linea.strip().startswith("#")


def contar_validas(texto):
    n = 0
    for l in texto.split("\n"):
        l = l.strip()
        if l and not l.startswith("#") and "=" in l:
            n += 1
    return n


def mayusculas_claves(config):
    return {k.upper(): v for k, v in config.items()}


def con_default_si_vacio(config, clave, defecto):
    v = config.get(clave, "")
    return v if v != "" else defecto


def claves_ordenadas(config):
    return sorted(config.keys())


def invertir(config):
    return {v: k for k, v in config.items()}
