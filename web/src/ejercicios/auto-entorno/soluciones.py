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
