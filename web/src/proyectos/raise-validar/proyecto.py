# Líder Grant — Validador de entradas (solución de referencia).
# El preamble (NIVELES_VALIDOS) está en meta.json y se antepone al corregir.

def validar_nivel(nivel):
    if nivel not in NIVELES_VALIDOS:
        raise ValueError("Nivel fuera de rango")
    return nivel

def validar_nombre(nombre):
    if not isinstance(nombre, str):
        raise ValueError("Nombre inválido")
    if nombre == "":
        raise ValueError("Nombre vacío")
    return nombre.lower()

def validar_tipo(tipo):
    tipos_validos = {"agua", "fuego", "planta", "roca", "bug", "normal"}
    if tipo not in tipos_validos:
        raise ValueError("Tipo desconocido")
    return tipo

def registrar_pokemon(nombre, tipo, nivel):
    return {
        "nombre": validar_nombre(nombre),
        "tipo": validar_tipo(tipo),
        "nivel": validar_nivel(nivel),
    }
