"""
✏️ Semana 06 — Ejercicios: Listas y Colecciones

Completá cada función donde dice '# TU CÓDIGO ACÁ'.
Énfasis en MANIPULAR datos: listas, sets, diccionarios y comprensiones.

Para probar tu trabajo: en test_ejercicios.py cambiá _cargar("soluciones")
por _cargar("ejercicios"). Respuestas en soluciones.py.
"""


# 1) Devolvé el PRIMER Pokémon del equipo. Si la lista está vacía, devolvé None.
def primer_pokemon(equipo):
    """Primer elemento de la lista, o None si está vacía."""
    # TU CÓDIGO ACÁ
    pass


# 2) Devolvé el ÚLTIMO Pokémon del equipo. Si está vacía, devolvé None.
def ultimo_pokemon(equipo):
    """Último elemento, o None si está vacía."""
    # TU CÓDIGO ACÁ
    pass


# 3) Agregá un Pokémon al final del equipo y devolvé la lista.
def agregar_pokemon(equipo, nombre):
    """Agregá 'nombre' al final de 'equipo' y devolvé la lista."""
    # TU CÓDIGO ACÁ
    pass


# 4) Devolvé cuántos Pokémon hay en el equipo.
def cantidad_pokemon(equipo):
    """Devolvé la cantidad de elementos del equipo."""
    # TU CÓDIGO ACÁ
    pass


# 5) Devolvé True si 'nombre' está en el equipo.
def esta_en_equipo(equipo, nombre):
    """Devolvé True/False según si 'nombre' está en la lista."""
    # TU CÓDIGO ACÁ
    pass


# 6) Quitá un Pokémon del equipo (si está) y devolvé la lista.
#    Si no está, devolvé la lista igual (sin romper).
def quitar_pokemon(equipo, nombre):
    """Sacá 'nombre' del equipo si está, y devolvé la lista."""
    # TU CÓDIGO ACÁ
    pass


# 7) Devolvé True si el equipo está LLENO (6 o más Pokémon).
def equipo_lleno(equipo):
    """Devolvé True si el equipo tiene 6 o más miembros."""
    # TU CÓDIGO ACÁ
    pass


# 8) Devolvé los tipos ÚNICOS, ordenados alfabéticamente, como una lista.
#    Ej: ["Fuego", "Agua", "Fuego"] -> ["Agua", "Fuego"]
def tipos_unicos(lista_tipos):
    """Devolvé una lista ordenada de tipos sin repetidos (usá un set)."""
    # TU CÓDIGO ACÁ
    pass


# 9) Contá cuántas veces aparece 'elemento' en la lista.
def contar_apariciones(lista, elemento):
    """Devolvé cuántas veces aparece 'elemento' en 'lista'."""
    # TU CÓDIGO ACÁ
    pass


# 10) Promedio de niveles. Si la lista está vacía, devolvé 0.
def promedio_niveles(niveles):
    """Devolvé el promedio de la lista de niveles, o 0 si está vacía."""
    # TU CÓDIGO ACÁ
    pass


# 11) Devolvé el nivel MÁXIMO de la lista. Si está vacía, devolvé None.
def nivel_maximo(niveles):
    """Devolvé el nivel más alto, o None si la lista está vacía."""
    # TU CÓDIGO ACÁ
    pass


# 12) Devolvé una lista con todos los nombres en MAYÚSCULAS.
#     Usá una comprensión de lista. Ej: ["pikachu"] -> ["PIKACHU"]
def nombres_en_mayuscula(equipo):
    """Devolvé los nombres en mayúscula (comprensión de lista)."""
    # TU CÓDIGO ACÁ
    pass


# 13) Devolvé solo los niveles que sean >= umbral (comprensión con filtro).
def niveles_altos(niveles, umbral):
    """Devolvé los niveles mayores o iguales al umbral."""
    # TU CÓDIGO ACÁ
    pass


# 14) Devolvé una lista de tuplas (indice, nombre) usando enumerate.
#     Ej: ["Pikachu", "Onix"] -> [(0, "Pikachu"), (1, "Onix")]
def equipo_numerado(equipo):
    """Devolvé pares (indice, nombre) con enumerate."""
    # TU CÓDIGO ACÁ
    pass


# 15) Creá un diccionario de un Pokémon con las claves nombre, tipo y nivel.
def crear_pokemon(nombre, tipo, nivel):
    """Devolvé un dict con claves 'nombre', 'tipo' y 'nivel'."""
    # TU CÓDIGO ACÁ
    pass


# 16) Obtené un dato del Pokémon de forma SEGURA. Si la clave no existe, devolvé None.
def obtener_dato(pokemon, clave):
    """Devolvé pokemon[clave] si existe, sino None (usá .get)."""
    # TU CÓDIGO ACÁ
    pass


# 17) Subí el nivel del Pokémon en 1 y devolvé el diccionario.
def subir_nivel(pokemon):
    """Sumá 1 a pokemon['nivel'] y devolvé el dict."""
    # TU CÓDIGO ACÁ
    pass


# 18) Recibí una lista de diccionarios (Pokémon) y devolvé solo sus nombres.
def nombres_de(pokemones):
    """Devolvé una lista con el 'nombre' de cada diccionario."""
    # TU CÓDIGO ACÁ
    pass


# 19) De una lista de Pokémon (dicts), devolvé los NOMBRES de los que sean del 'tipo' dado.
def nombres_por_tipo(pokemones, tipo):
    """Devolvé los nombres de los Pokémon cuyo 'tipo' coincide."""
    # TU CÓDIGO ACÁ
    pass


# 20) Ordená los Pokémon (dicts) por nivel de MAYOR a menor y devolvé sus nombres.
def nombres_por_nivel_desc(pokemones):
    """Devolvé los nombres ordenados por nivel, de mayor a menor."""
    # TU CÓDIGO ACÁ
    pass
