# Líder Koga — Código secreto ninja (solución de referencia).
# El preamble (CLAVE_NINJA) está en meta.json y se antepone al corregir.

def cifrar(mensaje):
    return "".join(CLAVE_NINJA.get(c, c) for c in mensaje)

def contar_palabras(texto):
    conteo = {}
    for palabra in texto.split():
        p = palabra.lower()
        conteo[p] = conteo.get(p, 0) + 1
    return conteo

def parsear_datos(linea):
    partes = linea.split("|")
    return {
        "nombre": partes[0].strip(),
        "tipo":   partes[1].strip(),
        "nivel":  int(partes[2].strip()),
    }

def procesar_informe(informe):
    resultado = []
    for linea in informe.split("\n"):
        if linea.strip() == "":
            continue
        poke = parsear_datos(linea)
        nombre_cifrado = cifrar(poke["nombre"])
        resultado.append("%s (nivel %d)" % (nombre_cifrado, poke["nivel"]))
    return resultado
