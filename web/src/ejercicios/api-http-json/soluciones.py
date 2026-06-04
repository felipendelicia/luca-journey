"""✅ Soluciones — APIs: HTTP y JSON"""
import json


def a_json(dato):
    return json.dumps(dato)


def de_json(texto):
    return json.loads(texto)


def extraer_nombre(texto):
    return json.loads(texto)["nombre"]


def es_exito(status):
    return 200 <= status < 300


def armar_respuesta(nombre, nivel):
    return {"nombre": nombre, "nivel": nivel}


def nombres(texto):
    return [p["nombre"] for p in json.loads(texto)]


def total_niveles(texto):
    return sum(p["nivel"] for p in json.loads(texto))
