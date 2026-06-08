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


def ultimo_resultado(texto):
    datos = json.loads(texto)
    return datos[-1] if datos else None


def nombres_de(texto):
    return [p["nombre"] for p in json.loads(texto)]


def ordenar_por_nivel(texto):
    datos = json.loads(texto)
    return [p["nombre"] for p in sorted(datos, key=lambda p: p["nivel"], reverse=True)]


def promedio_nivel(texto):
    datos = json.loads(texto)
    return sum(p["nivel"] for p in datos) / len(datos)


def mas_fuerte(texto):
    datos = json.loads(texto)
    return max(datos, key=lambda p: p["nivel"])["nombre"]


def existe(texto, nombre):
    return any(p["nombre"] == nombre for p in json.loads(texto))


def buscar(texto, nombre):
    for p in json.loads(texto):
        if p["nombre"] == nombre:
            return p
    return None


def tipos_unicos(texto):
    return sorted(set(p["tipo"] for p in json.loads(texto)))


def contar_por_tipo(texto):
    d = {}
    for p in json.loads(texto):
        d[p["tipo"]] = d.get(p["tipo"], 0) + 1
    return d


def filtrar_nivel_minimo(texto, minimo):
    return [p["nombre"] for p in json.loads(texto) if p["nivel"] >= minimo]


def hay_resultados(texto):
    return len(json.loads(texto)) > 0


def nombres_de_tipo(texto, tipo):
    return [p["nombre"] for p in json.loads(texto) if p["tipo"] == tipo]


def nivel_de(texto, nombre):
    for p in json.loads(texto):
        if p["nombre"] == nombre:
            return p["nivel"]
    return None


def resumen(texto):
    datos = json.loads(texto)
    return {"total": len(datos), "tipos": len(set(p["tipo"] for p in datos))}
