# Líder Roxanne — Enciclopedia JSON (solución de referencia).
import json

def armar_ficha(nombre, tipo, nivel):
    return {"nombre": nombre, "tipo": tipo, "nivel": nivel}

def ficha_a_json(nombre, tipo, nivel):
    ficha = {"nombre": nombre, "tipo": tipo, "nivel": nivel}
    return json.dumps(ficha)

def json_a_ficha(texto):
    d = json.loads(texto)
    return (d["nombre"], d["tipo"], d["nivel"])

def filtrar_fichas(lista_json, tipo):
    return [p["nombre"] for p in lista_json if p["tipo"] == tipo]
