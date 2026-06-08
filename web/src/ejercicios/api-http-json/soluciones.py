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


def con_indentacion(dato):
    return json.dumps(dato, indent=2)


def claves_json(texto):
    return list(json.loads(texto).keys())


def valor_de(texto, clave):
    return json.loads(texto).get(clave)


def cantidad_items(texto):
    return len(json.loads(texto))


def agregar_campo(texto, clave, valor):
    d = json.loads(texto)
    d[clave] = valor
    return json.dumps(d)


def es_json_valido(texto):
    try:
        json.loads(texto)
        return True
    except (ValueError, TypeError):
        return False


def ordenar_claves(dato):
    return json.dumps(dato, sort_keys=True)


def fusionar_json(a, b):
    da = json.loads(a)
    db = json.loads(b)
    da.update(db)
    return json.dumps(da)


def extraer_campo(texto, campo):
    return [item[campo] for item in json.loads(texto)]


def es_codigo_exito(status):
    return 200 <= status < 300


def es_codigo_error(status):
    return status >= 400


def clase_status(status):
    if 200 <= status < 300:
        return "exito"
    if 300 <= status < 400:
        return "redireccion"
    if 400 <= status < 500:
        return "cliente"
    return "servidor"


def contar_validos(textos):
    return sum(1 for t in textos if es_json_valido(t))
