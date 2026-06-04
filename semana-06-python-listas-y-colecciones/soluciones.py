"""
✅ Semana 06 — Soluciones: Listas y Colecciones

Comentadas línea por línea.
"""


# 1)
def primer_pokemon(equipo):
    """Primer elemento, o None si está vacía."""
    # Antes de acceder al índice 0, chequeamos que la lista NO esté vacía.
    if len(equipo) == 0:
        return None
    return equipo[0]


# 2)
def ultimo_pokemon(equipo):
    """Último elemento, o None si está vacía."""
    if len(equipo) == 0:
        return None
    # El índice -1 es el último elemento.
    return equipo[-1]


# 3)
def agregar_pokemon(equipo, nombre):
    """Agregá al final y devolvé la lista."""
    # .append() agrega un elemento al final de la lista.
    equipo.append(nombre)
    return equipo


# 4)
def cantidad_pokemon(equipo):
    """Cantidad de elementos."""
    # len() cuenta cuántos elementos tiene la lista.
    return len(equipo)


# 5)
def esta_en_equipo(equipo, nombre):
    """¿Está el nombre?"""
    # El operador 'in' chequea pertenencia y devuelve True/False.
    return nombre in equipo


# 6)
def quitar_pokemon(equipo, nombre):
    """Sacá el nombre si está."""
    # Solo intentamos remover si está, para no provocar un error.
    if nombre in equipo:
        equipo.remove(nombre)
    return equipo


# 7)
def equipo_lleno(equipo):
    """¿Tiene 6 o más?"""
    return len(equipo) >= 6


# 8)
def tipos_unicos(lista_tipos):
    """Tipos sin repetir, ordenados."""
    # set() elimina los duplicados; sorted() devuelve una lista ordenada.
    return sorted(set(lista_tipos))


# 9)
def contar_apariciones(lista, elemento):
    """Cuántas veces aparece."""
    # .count() cuenta las apariciones de un valor en la lista.
    return lista.count(elemento)


# 10)
def promedio_niveles(niveles):
    """Promedio, o 0 si está vacía."""
    # Evitamos dividir por cero cuando la lista está vacía.
    if len(niveles) == 0:
        return 0
    # sum() suma todos; dividimos por la cantidad.
    return sum(niveles) / len(niveles)


# 11)
def nivel_maximo(niveles):
    """Máximo, o None si está vacía."""
    if len(niveles) == 0:
        return None
    # max() devuelve el valor más grande de la lista.
    return max(niveles)


# 12)
def nombres_en_mayuscula(equipo):
    """Nombres en mayúscula (comprensión)."""
    # Por cada nombre 'n' de la lista, generamos n.upper().
    return [n.upper() for n in equipo]


# 13)
def niveles_altos(niveles, umbral):
    """Niveles >= umbral (comprensión con filtro)."""
    # El 'if' al final filtra: solo entran los que cumplen la condición.
    return [n for n in niveles if n >= umbral]


# 14)
def equipo_numerado(equipo):
    """Pares (indice, nombre)."""
    # enumerate da (indice, valor); list() lo convierte en lista de tuplas.
    return list(enumerate(equipo))


# 15)
def crear_pokemon(nombre, tipo, nivel):
    """Diccionario de un Pokémon."""
    # Un diccionario asocia claves a valores.
    return {"nombre": nombre, "tipo": tipo, "nivel": nivel}


# 16)
def obtener_dato(pokemon, clave):
    """Dato seguro con .get."""
    # .get() devuelve None (o un default) si la clave no existe, sin romper.
    return pokemon.get(clave)


# 17)
def subir_nivel(pokemon):
    """Sumá 1 al nivel."""
    # Accedemos al valor actual y le sumamos 1.
    pokemon["nivel"] = pokemon["nivel"] + 1
    return pokemon


# 18)
def nombres_de(pokemones):
    """Nombres de cada dict."""
    # Por cada diccionario 'p', sacamos su clave 'nombre'.
    return [p["nombre"] for p in pokemones]


# 19)
def nombres_por_tipo(pokemones, tipo):
    """Nombres de los del tipo dado."""
    # Comprensión con filtro: solo los que tienen ese 'tipo'.
    return [p["nombre"] for p in pokemones if p["tipo"] == tipo]


# 20)
def nombres_por_nivel_desc(pokemones):
    """Nombres ordenados por nivel, de mayor a menor."""
    # sorted con key=... ordena según el nivel; reverse=True lo hace descendente.
    ordenados = sorted(pokemones, key=lambda p: p["nivel"], reverse=True)
    # Devolvemos solo los nombres de la lista ya ordenada.
    return [p["nombre"] for p in ordenados]
