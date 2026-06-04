"""
✏️ Semana 07 — Ejercicios: Cadenas y Archivos

Completá cada función donde dice '# TU CÓDIGO ACÁ'.
Las funciones de archivos reciben la RUTA como parámetro (así los tests usan
archivos temporales). Respuestas en soluciones.py.

Para probar tu trabajo: en test_ejercicios.py cambiá _cargar("soluciones")
por _cargar("ejercicios").
"""


# ----------------------------------------------------------------------
# STRINGS
# ----------------------------------------------------------------------

# 1) Devolvé el texto en MAYÚSCULAS.
def a_mayusculas(texto):
    """Devolvé el texto en mayúsculas."""
    # TU CÓDIGO ACÁ
    pass


# 2) Sacá los espacios del principio y del final.
def limpiar_espacios(texto):
    """Devolvé el texto sin espacios en los bordes."""
    # TU CÓDIGO ACÁ
    pass


# 3) Reemplazá todas las apariciones de 'viejo' por 'nuevo'.
def reemplazar(texto, viejo, nuevo):
    """Devolvé el texto con 'viejo' cambiado por 'nuevo'."""
    # TU CÓDIGO ACÁ
    pass


# 4) Separá una línea CSV en una lista, usando la coma.
#    "Pikachu,Electrico,25" -> ["Pikachu", "Electrico", "25"]
def separar_csv(linea):
    """Devolvé la lista de partes separadas por coma."""
    # TU CÓDIGO ACÁ
    pass


# 5) Uní una lista en una línea CSV separada por comas.
#    ["Charizard", "Fuego", 50] -> "Charizard,Fuego,50"
def unir_csv(lista):
    """Devolvé los elementos unidos por comas (convertí cada uno a str)."""
    # TU CÓDIGO ACÁ
    pass


# 6) Devolvé el texto invertido (al revés).
def invertir(texto):
    """Devolvé el texto dado vuelta. Pista: slicing [::-1]."""
    # TU CÓDIGO ACÁ
    pass


# 7) Devolvé la cantidad de caracteres del texto.
def cantidad_caracteres(texto):
    """Devolvé la longitud del texto."""
    # TU CÓDIGO ACÁ
    pass


# 8) Devolvé True si el texto empieza con 'prefijo'.
def empieza_con(texto, prefijo):
    """Devolvé True/False usando startswith."""
    # TU CÓDIGO ACÁ
    pass


# 9) Devolvé las primeras n letras del texto (slicing).
def primeras_letras(texto, n):
    """Devolvé texto[:n]."""
    # TU CÓDIGO ACÁ
    pass


# 10) Devolvé las últimas n letras del texto (slicing).
def ultimas_letras(texto, n):
    """Devolvé las últimas n letras."""
    # TU CÓDIGO ACÁ
    pass


# 11) Devolvé el texto con la primera letra en mayúscula y el resto en minúscula.
#     "pikachu" -> "Pikachu" ; "CHARIZARD" -> "Charizard"
def capitalizar(texto):
    """Devolvé el texto capitalizado."""
    # TU CÓDIGO ACÁ
    pass


# 12) Contá cuántas veces aparece 'sub' dentro de 'texto'.
def contar_subtexto(texto, sub):
    """Devolvé la cantidad de apariciones de 'sub'."""
    # TU CÓDIGO ACÁ
    pass


# 13) Convertí un texto a entero de forma SEGURA. Si no se puede, devolvé 'default'.
#     Usá try/except. convertir_entero_seguro("25") -> 25 ; ("abc") -> 0
def convertir_entero_seguro(texto, default=0):
    """Devolvé int(texto), o 'default' si falla (try/except ValueError)."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# ARCHIVOS (reciben la ruta como parámetro)
# ----------------------------------------------------------------------

# 14) Escribí 'texto' en el archivo 'ruta' (reemplazando lo que hubiera). Usá with.
def escribir_texto(ruta, texto):
    """Escribí 'texto' en el archivo. No devuelve nada."""
    # TU CÓDIGO ACÁ
    pass


# 15) Leé y devolvé TODO el contenido del archivo 'ruta'. Usá with.
def leer_texto(ruta):
    """Devolvé el contenido completo del archivo."""
    # TU CÓDIGO ACÁ
    pass


# 16) Agregá 'linea' al final del archivo (con un salto de línea \n al final).
#     Usá el modo "a" (append).
def agregar_linea(ruta, linea):
    """Agregá 'linea' + '\\n' al final del archivo."""
    # TU CÓDIGO ACÁ
    pass


# 17) Contá cuántas líneas tiene el archivo.
def contar_lineas(ruta):
    """Devolvé la cantidad de líneas del archivo."""
    # TU CÓDIGO ACÁ
    pass


# 18) Guardá una lista en el archivo, un elemento por línea.
def guardar_lista(ruta, lista):
    """Escribí cada elemento de 'lista' en una línea distinta."""
    # TU CÓDIGO ACÁ
    pass


# 19) Cargá una lista desde el archivo (una línea = un elemento, sin el \n).
#     Si el archivo NO existe, devolvé una lista vacía (usá try/except).
def cargar_lista(ruta):
    """Devolvé la lista de líneas del archivo, o [] si no existe."""
    # TU CÓDIGO ACÁ
    pass


# 20) Parseá una línea de Pokémon "nombre,tipo,nivel" a un diccionario.
#     "Pikachu,Electrico,25" -> {"nombre": "Pikachu", "tipo": "Electrico", "nivel": 25}
#     OJO: el nivel debe quedar como int.
def parsear_pokemon(linea):
    """Devolvé un dict con nombre, tipo y nivel (nivel como int)."""
    # TU CÓDIGO ACÁ
    pass
