"""✏️ Ejercicios — Listas y Colecciones

Manipular datos: listas, sets, diccionarios y comprensiones. ✅ Corregir al terminar.
"""


# El primero del equipo
# Devolvé el PRIMER Pokémon de la lista. Si está vacía, devolvé None.
# Ejemplo:  primer_pokemon(["Pikachu", "Onix"])  →  "Pikachu"   ·   primer_pokemon([])  →  None
def primer_pokemon(equipo):
    """Primer elemento de la lista, o None si está vacía."""
    # TU CÓDIGO ACÁ
    pass


# El último del equipo
# Devolvé el ÚLTIMO Pokémon. Si está vacía, devolvé None.
# Ejemplo:  ultimo_pokemon(["Pikachu", "Onix"])  →  "Onix"   ·   ultimo_pokemon([])  →  None
def ultimo_pokemon(equipo):
    """Último elemento, o None si está vacía."""
    # TU CÓDIGO ACÁ
    pass


# Sumar al equipo
# Agregá 'nombre' al final del equipo y devolvé la lista.
# Ejemplo:  agregar_pokemon(["Pikachu"], "Eevee")  →  ["Pikachu", "Eevee"]
def agregar_pokemon(equipo, nombre):
    """Agregá 'nombre' al final y devolvé la lista."""
    # TU CÓDIGO ACÁ
    pass


# ¿Cuántos hay?
# Devolvé cuántos Pokémon tiene el equipo.
# Ejemplo:  cantidad_pokemon(["Pikachu", "Onix"])  →  2
def cantidad_pokemon(equipo):
    """Devolvé la cantidad de elementos."""
    # TU CÓDIGO ACÁ
    pass


# ¿Está en el equipo?
# Devolvé True si 'nombre' está en el equipo.
# Ejemplo:  esta_en_equipo(["Pikachu", "Onix"], "Onix")  →  True
def esta_en_equipo(equipo, nombre):
    """Devolvé True/False según si 'nombre' está en la lista."""
    # TU CÓDIGO ACÁ
    pass


# Liberar Pokémon
# Quitá 'nombre' del equipo si está, y devolvé la lista. Si no está, devolvela igual.
# Ejemplo:  quitar_pokemon(["Pikachu", "Onix"], "Onix")  →  ["Pikachu"]
def quitar_pokemon(equipo, nombre):
    """Sacá 'nombre' del equipo si está, y devolvé la lista."""
    # TU CÓDIGO ACÁ
    pass


# ¿Equipo lleno?
# Devolvé True si el equipo tiene 6 o más Pokémon.
# Ejemplo:  equipo_lleno(["a", "b", "c", "d", "e", "f"])  →  True
def equipo_lleno(equipo):
    """Devolvé True si el equipo tiene 6 o más miembros."""
    # TU CÓDIGO ACÁ
    pass


# Tipos únicos
# Devolvé los tipos SIN repetir, ordenados alfabéticamente. Pista: usá un set y sorted.
# Ejemplo:  tipos_unicos(["Fuego", "Agua", "Fuego"])  →  ["Agua", "Fuego"]
def tipos_unicos(lista_tipos):
    """Devolvé una lista ordenada de tipos sin repetidos."""
    # TU CÓDIGO ACÁ
    pass


# Contar apariciones
# Devolvé cuántas veces aparece 'elemento' en la lista.
# Ejemplo:  contar_apariciones(["a", "b", "a"], "a")  →  2
def contar_apariciones(lista, elemento):
    """Devolvé cuántas veces aparece 'elemento'."""
    # TU CÓDIGO ACÁ
    pass


# Promedio de niveles
# Devolvé el promedio de la lista de niveles. Si está vacía, devolvé 0.
# Ejemplo:  promedio_niveles([10, 20, 30])  →  20.0   ·   promedio_niveles([])  →  0
def promedio_niveles(niveles):
    """Devolvé el promedio, o 0 si está vacía."""
    # TU CÓDIGO ACÁ
    pass


# Nivel máximo
# Devolvé el nivel más alto de la lista. Si está vacía, devolvé None.
# Ejemplo:  nivel_maximo([12, 45, 30])  →  45   ·   nivel_maximo([])  →  None
def nivel_maximo(niveles):
    """Devolvé el nivel más alto, o None si está vacía."""
    # TU CÓDIGO ACÁ
    pass


# Nombres en MAYÚSCULA
# Devolvé una lista con todos los nombres en mayúsculas. Usá una comprensión de lista.
# Ejemplo:  nombres_en_mayuscula(["pikachu", "onix"])  →  ["PIKACHU", "ONIX"]
def nombres_en_mayuscula(equipo):
    """Devolvé los nombres en mayúscula (comprensión de lista)."""
    # TU CÓDIGO ACÁ
    pass


# Niveles altos
# Devolvé solo los niveles que sean >= umbral. Usá una comprensión con filtro.
# Ejemplo:  niveles_altos([10, 40, 25], 30)  →  [40]
def niveles_altos(niveles, umbral):
    """Devolvé los niveles mayores o iguales al umbral."""
    # TU CÓDIGO ACÁ
    pass


# Equipo numerado
# Devolvé pares (indice, nombre) usando enumerate.
# Ejemplo:  equipo_numerado(["Pikachu", "Onix"])  →  [(0, "Pikachu"), (1, "Onix")]
def equipo_numerado(equipo):
    """Devolvé pares (indice, nombre) con enumerate."""
    # TU CÓDIGO ACÁ
    pass


# Crear un Pokémon (diccionario)
# Devolvé un dict con las claves 'nombre', 'tipo' y 'nivel'.
# Ejemplo:  crear_pokemon("Pikachu", "Electrico", 25)  →  {"nombre": "Pikachu", "tipo": "Electrico", "nivel": 25}
def crear_pokemon(nombre, tipo, nivel):
    """Devolvé un dict con 'nombre', 'tipo' y 'nivel'."""
    # TU CÓDIGO ACÁ
    pass


# Dato seguro
# Devolvé pokemon[clave] si existe; si no, devolvé None. Pista: usá .get(...).
# Ejemplo:  obtener_dato({"nivel": 25}, "tipo")  →  None
def obtener_dato(pokemon, clave):
    """Devolvé pokemon[clave] si existe, sino None."""
    # TU CÓDIGO ACÁ
    pass


# Subir el nivel
# Sumale 1 al nivel del Pokémon y devolvé el diccionario.
# Ejemplo:  subir_nivel({"nivel": 25})  →  {"nivel": 26}
def subir_nivel(pokemon):
    """Sumá 1 a pokemon['nivel'] y devolvé el dict."""
    # TU CÓDIGO ACÁ
    pass


# Solo los nombres
# 'pokemones' es una lista de diccionarios. Devolvé una lista con el 'nombre' de cada uno.
# Ejemplo:  nombres_de([{"nombre": "Pikachu"}, {"nombre": "Onix"}])  →  ["Pikachu", "Onix"]
def nombres_de(pokemones):
    """Devolvé una lista con el 'nombre' de cada dict."""
    # TU CÓDIGO ACÁ
    pass


# Nombres por tipo
# De una lista de Pokémon (dicts), devolvé los NOMBRES de los que sean del 'tipo' dado.
# Ejemplo:  nombres_por_tipo([{"nombre":"Vulpix","tipo":"Fuego"}], "Fuego")  →  ["Vulpix"]
def nombres_por_tipo(pokemones, tipo):
    """Devolvé los nombres de los Pokémon de ese 'tipo'."""
    # TU CÓDIGO ACÁ
    pass


# Ranking por nivel
# Ordená los Pokémon (dicts) por nivel de MAYOR a menor y devolvé sus nombres.
# Ejemplo:  nombres_por_nivel_desc([{"nombre":"A","nivel":10},{"nombre":"B","nivel":90}])  →  ["B", "A"]
def nombres_por_nivel_desc(pokemones):
    """Devolvé los nombres ordenados por nivel, de mayor a menor."""
    # TU CÓDIGO ACÁ
    pass
