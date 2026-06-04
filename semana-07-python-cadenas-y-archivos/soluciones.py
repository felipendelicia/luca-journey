"""
✅ Semana 07 — Soluciones: Cadenas y Archivos

Comentadas línea por línea.
"""


# ----------------------------------------------------------------------
# STRINGS
# ----------------------------------------------------------------------

# 1)
def a_mayusculas(texto):
    """Texto en mayúsculas."""
    # .upper() devuelve una copia en mayúsculas (no toca el original).
    return texto.upper()


# 2)
def limpiar_espacios(texto):
    """Sin espacios en los bordes."""
    # .strip() saca espacios (y saltos de línea) del principio y el final.
    return texto.strip()


# 3)
def reemplazar(texto, viejo, nuevo):
    """Cambiá 'viejo' por 'nuevo'."""
    # .replace() reemplaza TODAS las apariciones.
    return texto.replace(viejo, nuevo)


# 4)
def separar_csv(linea):
    """Separar por coma."""
    # .split(",") corta el texto cada vez que encuentra una coma.
    return linea.split(",")


# 5)
def unir_csv(lista):
    """Unir con comas."""
    # join solo une strings, así que convertimos cada elemento con str().
    return ",".join(str(elemento) for elemento in lista)


# 6)
def invertir(texto):
    """Texto al revés."""
    # El slicing [::-1] recorre el texto con paso -1: de atrás para adelante.
    return texto[::-1]


# 7)
def cantidad_caracteres(texto):
    """Longitud del texto."""
    return len(texto)


# 8)
def empieza_con(texto, prefijo):
    """¿Empieza con prefijo?"""
    return texto.startswith(prefijo)


# 9)
def primeras_letras(texto, n):
    """Primeras n letras."""
    # texto[:n] toma desde el inicio hasta la posición n (sin incluirla).
    return texto[:n]


# 10)
def ultimas_letras(texto, n):
    """Últimas n letras."""
    # texto[-n:] toma las últimas n letras.
    return texto[-n:]


# 11)
def capitalizar(texto):
    """Primera en mayúscula, resto en minúscula."""
    # .capitalize() hace exactamente eso.
    return texto.capitalize()


# 12)
def contar_subtexto(texto, sub):
    """Apariciones de 'sub'."""
    return texto.count(sub)


# 13)
def convertir_entero_seguro(texto, default=0):
    """int seguro con try/except."""
    try:
        # Intentamos convertir. Si el texto no es un número, salta ValueError.
        return int(texto)
    except ValueError:
        # Si falló, devolvemos el valor por defecto en vez de romper.
        return default


# ----------------------------------------------------------------------
# ARCHIVOS
# ----------------------------------------------------------------------

# 14)
def escribir_texto(ruta, texto):
    """Escribir (reemplazando)."""
    # Modo "w" crea o reemplaza. 'with' cierra el archivo solo.
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(texto)


# 15)
def leer_texto(ruta):
    """Leer todo."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        return archivo.read()


# 16)
def agregar_linea(ruta, linea):
    """Agregar al final."""
    # Modo "a" (append) escribe al final sin borrar lo anterior.
    with open(ruta, "a", encoding="utf-8") as archivo:
        archivo.write(linea + "\n")


# 17)
def contar_lineas(ruta):
    """Contar líneas."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        # readlines() devuelve una lista con todas las líneas.
        return len(archivo.readlines())


# 18)
def guardar_lista(ruta, lista):
    """Guardar lista, una por línea."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        for elemento in lista:
            archivo.write(str(elemento) + "\n")


# 19)
def cargar_lista(ruta):
    """Cargar lista, o [] si no existe."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            # Por cada línea, le sacamos el \n con strip().
            return [linea.strip() for linea in archivo]
    except FileNotFoundError:
        # Si el archivo no existe, devolvemos lista vacía en vez de romper.
        return []


# 20)
def parsear_pokemon(linea):
    """Línea CSV a diccionario."""
    # Separamos los tres campos.
    nombre, tipo, nivel = linea.strip().split(",")
    # Armamos el diccionario; convertimos el nivel a entero.
    return {"nombre": nombre, "tipo": tipo, "nivel": int(nivel)}
