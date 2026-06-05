# Líder Tate y Liza — Procesar respuestas de API (solución de referencia).

def extraer_nombre_nivel(respuesta):
    return (respuesta["nombre"], respuesta["nivel"])

def filtrar_por_tipo(lista, tipo):
    return [p["nombre"] for p in lista if p["tipo"] == tipo]

def manejar_respuesta(status, datos):
    if status == 200:
        return datos
    return None

def resumen_equipo(lista):
    return ["%s (tipo: %s, nivel: %d)" % (p["nombre"], p["tipo"], p["nivel"]) for p in lista]
