"""✏️ Ejercicios — SQL: filtrar y ordenar

WHERE para filtrar, ORDER BY para ordenar, LIKE para buscar texto, LIMIT para cortar.
La tabla 'pokemon' tiene: nombre, nivel, tipo. ✅ Corregir al terminar.
"""
import sqlite3


# Filtrar por tipo
# Devolvé los nombres de los Pokémon de un tipo dado. Usá WHERE con parámetro (?).
# Ejemplo:  de_tipo(con, "Fuego")  →  ["Charizard", "Vulpix"]
def de_tipo(conexion, tipo):
    """Devolvé los nombres donde tipo = el pedido."""
    # TU CÓDIGO ACÁ
    pass


# Los fuertes, ordenados
# Nombres con nivel >= mínimo, ordenados de mayor a menor nivel.
# Pista: WHERE nivel >= ? ORDER BY nivel DESC.
# Ejemplo:  fuertes(con, 50)  →  ["Charizard", "Snorlax"]
def fuertes(conexion, minimo):
    """Devolvé los nombres con nivel >= mínimo, de mayor a menor."""
    # TU CÓDIGO ACÁ
    pass


# Ordenar por nivel
# Devolvé todos los nombres ordenados por nivel descendente. Pista: ORDER BY nivel DESC.
def ordenados_por_nivel(conexion):
    """Devolvé los nombres ordenados por nivel (mayor a menor)."""
    # TU CÓDIGO ACÁ
    pass


# Empiezan con…
# Devolvé los nombres que empiezan con una letra dada. Pista: WHERE nombre LIKE ? (letra + '%').
# Ejemplo:  empiezan_con(con, "C")  →  ["Charizard", "Charmander"]
def empiezan_con(conexion, letra):
    """Devolvé los nombres que empiezan con 'letra'."""
    # TU CÓDIGO ACÁ
    pass


# Top n
# Devolvé los n Pokémon de mayor nivel (nombres). Pista: ORDER BY nivel DESC LIMIT ?.
# Ejemplo:  top(con, 2)  →  los 2 de mayor nivel
def top(conexion, n):
    """Devolvé los nombres de los n de mayor nivel."""
    # TU CÓDIGO ACÁ
    pass


# Débiles
# Devolvé los NOMBRES con nivel menor o igual a `maximo`. Pista: WHERE nivel <= ?.
def debiles(conexion, maximo):
    """Devolvé los nombres con nivel <= maximo."""
    # TU CÓDIGO ACÁ
    pass


# Entre dos niveles
# Devolvé los NOMBRES con nivel entre `lo` y `hi` (incluidos). Pista: WHERE nivel BETWEEN ? AND ?.
def entre_niveles(conexion, lo, hi):
    """Devolvé los nombres con nivel entre lo y hi."""
    # TU CÓDIGO ACÁ
    pass


# Que NO son de un tipo
# Devolvé los NOMBRES cuyo tipo NO sea `tipo`. Pista: WHERE tipo != ?.
def no_de_tipo(conexion, tipo):
    """Devolvé los nombres que no son de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Que contienen un texto
# Devolvé los NOMBRES que contengan `sub`. Pista: WHERE nombre LIKE ? con "%sub%".
def contienen(conexion, sub):
    """Devolvé los nombres que contienen sub."""
    # TU CÓDIGO ACÁ
    pass


# Ordenados alfabéticamente
# Devolvé los NOMBRES ordenados de la A a la Z. Pista: ORDER BY nombre.
def ordenados_alfabeticamente(conexion):
    """Devolvé los nombres ordenados alfabéticamente."""
    # TU CÓDIGO ACÁ
    pass


# El último alfabéticamente
# Devolvé el NOMBRE que va último en orden alfabético. Pista: ORDER BY nombre DESC LIMIT 1.
def ultimo_alfabetico(conexion):
    """Devolvé el último nombre alfabéticamente."""
    # TU CÓDIGO ACÁ
    pass


# Nombre y tipo
# Devolvé una lista de tuplas (nombre, tipo). Pista: SELECT nombre, tipo ...
def nombres_y_tipos(conexion):
    """Devolvé pares (nombre, tipo)."""
    # TU CÓDIGO ACÁ
    pass


# De dos tipos
# Devolvé los NOMBRES de los Pokémon que sean de tipo `t1` o `t2`. Pista: WHERE tipo IN (?, ?).
def dos_tipos(conexion, t1, t2):
    """Devolvé los nombres de tipo t1 o t2."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad por encima de un nivel
# Devolvé cuántos Pokémon tienen nivel mayor que `n`. Pista: SELECT COUNT(*) ... WHERE nivel > ?.
def cantidad_por_encima(conexion, n):
    """Devolvé cuántos tienen nivel > n."""
    # TU CÓDIGO ACÁ
    pass


# Nombres largos
# Devolvé los NOMBRES con más de `largo` caracteres. Pista: WHERE LENGTH(nombre) > ?.
def nombres_largos(conexion, largo):
    """Devolvé los nombres de más de `largo` caracteres."""
    # TU CÓDIGO ACÁ
    pass


# El de cierto nivel
# Devolvé el NOMBRE del Pokémon cuyo nivel sea exactamente `nivel`, o None si no hay.
def el_de_nivel(conexion, nivel):
    """Devolvé el nombre del de ese nivel, o None."""
    # TU CÓDIGO ACÁ
    pass


# Tipos distintos
# Devolvé los tipos distintos ORDENADOS. Pista: SELECT DISTINCT tipo ... ORDER BY tipo.
def distintos_tipos(conexion):
    """Devolvé los tipos distintos, ordenados."""
    # TU CÓDIGO ACÁ
    pass


# Los n más débiles
# Devolvé los NOMBRES de los `n` Pokémon de MENOR nivel. Pista: ORDER BY nivel ASC LIMIT ?.
def los_n_mas_debiles(conexion, n):
    """Devolvé los n de menor nivel."""
    # TU CÓDIGO ACÁ
    pass


# El más fuerte de un tipo
# Devolvé el NOMBRE del Pokémon de mayor nivel del tipo `tipo`, o None si no hay.
def mas_fuerte_de_tipo(conexion, tipo):
    """Devolvé el más fuerte de ese tipo, o None."""
    # TU CÓDIGO ACÁ
    pass


# Ordenar por tipo y nombre
# Devolvé los NOMBRES ordenados primero por tipo, y dentro de cada tipo, alfabéticamente.
# Pista: ORDER BY tipo, nombre.
def ordenar_por_tipo(conexion):
    """Devolvé los nombres ordenados por tipo y nombre."""
    # TU CÓDIGO ACÁ
    pass
