"""✏️ Ejercicios — Cadenas y Archivos

Manipular texto y leer/escribir archivos. Las funciones de archivo reciben la RUTA
como parámetro (los tests usan archivos temporales). ✅ Corregir al terminar.
"""


# ── Texto (strings) ──

# A MAYÚSCULAS
# Devolvé el texto en mayúsculas.
# Ejemplo:  a_mayusculas("pikachu")  →  "PIKACHU"
def a_mayusculas(texto):
    """Devolvé el texto en mayúsculas."""
    # TU CÓDIGO ACÁ
    pass


# Limpiar espacios
# Sacá los espacios del principio y del final.
# Ejemplo:  limpiar_espacios("  Pika  ")  →  "Pika"
def limpiar_espacios(texto):
    """Devolvé el texto sin espacios en los bordes."""
    # TU CÓDIGO ACÁ
    pass


# Buscar y reemplazar
# Reemplazá todas las apariciones de 'viejo' por 'nuevo'.
# Ejemplo:  reemplazar("Pika Pika", "Pika", "Chu")  →  "Chu Chu"
def reemplazar(texto, viejo, nuevo):
    """Devolvé el texto con 'viejo' cambiado por 'nuevo'."""
    # TU CÓDIGO ACÁ
    pass


# Separar CSV
# Separá una línea por las comas y devolvé la lista de partes.
# Ejemplo:  separar_csv("Pikachu,Electrico,25")  →  ["Pikachu", "Electrico", "25"]
def separar_csv(linea):
    """Devolvé la lista de partes separadas por coma."""
    # TU CÓDIGO ACÁ
    pass


# Unir CSV
# Uní una lista en una línea separada por comas (convertí cada elemento a texto).
# Ejemplo:  unir_csv(["Charizard", "Fuego", 50])  →  "Charizard,Fuego,50"
def unir_csv(lista):
    """Devolvé los elementos unidos por comas."""
    # TU CÓDIGO ACÁ
    pass


# Texto al revés
# Devolvé el texto invertido. Pista: slicing [::-1].
# Ejemplo:  invertir("Pikachu")  →  "uhcakiP"
def invertir(texto):
    """Devolvé el texto dado vuelta."""
    # TU CÓDIGO ACÁ
    pass


# Contar caracteres
# Devolvé cuántos caracteres tiene el texto.
# Ejemplo:  cantidad_caracteres("Pikachu")  →  7
def cantidad_caracteres(texto):
    """Devolvé la longitud del texto."""
    # TU CÓDIGO ACÁ
    pass


# ¿Empieza con…?
# Devolvé True si el texto empieza con 'prefijo'. Pista: startswith.
# Ejemplo:  empieza_con("Charizard", "Char")  →  True
def empieza_con(texto, prefijo):
    """Devolvé True/False usando startswith."""
    # TU CÓDIGO ACÁ
    pass


# Primeras n letras
# Devolvé las primeras n letras del texto (slicing).
# Ejemplo:  primeras_letras("Charizard", 4)  →  "Char"
def primeras_letras(texto, n):
    """Devolvé texto[:n]."""
    # TU CÓDIGO ACÁ
    pass


# Últimas n letras
# Devolvé las últimas n letras del texto (slicing).
# Ejemplo:  ultimas_letras("Charizard", 3)  →  "ard"
def ultimas_letras(texto, n):
    """Devolvé las últimas n letras."""
    # TU CÓDIGO ACÁ
    pass


# Capitalizar
# Devolvé el texto con la primera letra en mayúscula y el resto en minúscula.
# Ejemplo:  capitalizar("CHARIZARD")  →  "Charizard"   ·   capitalizar("pikachu")  →  "Pikachu"
def capitalizar(texto):
    """Devolvé el texto capitalizado."""
    # TU CÓDIGO ACÁ
    pass


# Contar subtexto
# Contá cuántas veces aparece 'sub' dentro de 'texto'.
# Ejemplo:  contar_subtexto("banana", "a")  →  3
def contar_subtexto(texto, sub):
    """Devolvé la cantidad de apariciones de 'sub'."""
    # TU CÓDIGO ACÁ
    pass


# Convertir seguro
# Convertí 'texto' a int. Si no se puede, devolvé 'default'. Usá try/except.
# Ejemplo:  convertir_entero_seguro("25")  →  25   ·   convertir_entero_seguro("abc")  →  0
def convertir_entero_seguro(texto, default=0):
    """Devolvé int(texto), o 'default' si falla."""
    # TU CÓDIGO ACÁ
    pass


# ── Archivos (reciben la ruta como parámetro) ──

# Escribir un archivo
# Escribí 'texto' en el archivo 'ruta' (reemplazando lo que hubiera). Usá with open(...).
# Ejemplo:  escribir_texto("equipo.txt", "Pikachu")  escribe "Pikachu" en el archivo.
def escribir_texto(ruta, texto):
    """Escribí 'texto' en el archivo. No devuelve nada."""
    # TU CÓDIGO ACÁ
    pass


# Leer un archivo
# Leé y devolvé TODO el contenido del archivo 'ruta'. Usá with open(...).
# Ejemplo:  si el archivo dice "Pikachu"  →  leer_texto(ruta)  →  "Pikachu"
def leer_texto(ruta):
    """Devolvé el contenido completo del archivo."""
    # TU CÓDIGO ACÁ
    pass


# Agregar una línea
# Agregá 'linea' al final del archivo, con un salto de línea. Usá el modo "a" (append).
# Ejemplo:  agregar_linea("dex.txt", "Onix")  suma una línea "Onix" al final.
def agregar_linea(ruta, linea):
    """Agregá 'linea' + salto de línea al final del archivo."""
    # TU CÓDIGO ACÁ
    pass


# Contar líneas
# Devolvé cuántas líneas tiene el archivo.
# Ejemplo:  un archivo con 3 líneas  →  contar_lineas(ruta)  →  3
def contar_lineas(ruta):
    """Devolvé la cantidad de líneas del archivo."""
    # TU CÓDIGO ACÁ
    pass


# Guardar una lista
# Escribí cada elemento de 'lista' en una línea distinta del archivo.
# Ejemplo:  guardar_lista("eq.txt", ["Pikachu", "Onix"])  escribe dos líneas.
def guardar_lista(ruta, lista):
    """Escribí cada elemento en su propia línea."""
    # TU CÓDIGO ACÁ
    pass


# Cargar una lista
# Devolvé la lista de líneas del archivo (sin el salto de línea). Si el archivo NO existe,
# devolvé una lista vacía. Usá try/except.
# Ejemplo:  archivo con "Pikachu\nOnix"  →  ["Pikachu", "Onix"]   ·   no existe  →  []
def cargar_lista(ruta):
    """Devolvé la lista de líneas, o [] si no existe."""
    # TU CÓDIGO ACÁ
    pass


# Parsear un Pokémon
# Convertí una línea "nombre,tipo,nivel" en un diccionario. El nivel debe quedar como int.
# Ejemplo:  parsear_pokemon("Pikachu,Electrico,25")  →  {"nombre": "Pikachu", "tipo": "Electrico", "nivel": 25}
def parsear_pokemon(linea):
    """Devolvé un dict con nombre, tipo y nivel (nivel como int)."""
    # TU CÓDIGO ACÁ
    pass
