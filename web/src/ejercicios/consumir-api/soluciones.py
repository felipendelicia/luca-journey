"""✅ Soluciones — Consumir una API"""
import json


def extraer_tipos(texto):
    return json.loads(texto)["tipos"]


def nombre_y_nivel(texto):
    d = json.loads(texto)
    return (d["nombre"], d["nivel"])


def filtrar_por_tipo(texto, tipo):
    lista = json.loads(texto)
    return [p["nombre"] for p in lista if p["tipo"] == tipo]


def manejar_respuesta(status, texto):
    if status == 200:
        return json.loads(texto)
    return None


def contar_resultados(texto):
    return len(json.loads(texto)["results"])


def primer_resultado(texto):
    return json.loads(texto)["results"][0]["name"]
