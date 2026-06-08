"""✏️ Ejercicios — Módulos y pip

Usar módulos de la librería estándar (math, random, json, datetime, os) y tu propio
módulo pokeutils. ✅ Corregir al terminar.
"""

import math
import random
import json
import os
from datetime import date

import pokeutils  # nuestro módulo propio (está al lado de este archivo)


# Raíz cuadrada
# Devolvé la raíz cuadrada de n. Pista: math.sqrt(n).
# Ejemplo:  raiz_cuadrada(9)  →  3.0
def raiz_cuadrada(n):
    """Devolvé la raíz cuadrada de n."""
    # TU CÓDIGO ACÁ
    pass


# Redondear para arriba
# Redondeá n hacia arriba. Pista: math.ceil.
# Ejemplo:  redondear_arriba(4.1)  →  5
def redondear_arriba(n):
    """Devolvé n redondeado hacia arriba."""
    # TU CÓDIGO ACÁ
    pass


# Redondear para abajo
# Redondeá n hacia abajo. Pista: math.floor.
# Ejemplo:  redondear_abajo(4.9)  →  4
def redondear_abajo(n):
    """Devolvé n redondeado hacia abajo."""
    # TU CÓDIGO ACÁ
    pass


# Pi con 2 decimales
# Devolvé math.pi redondeado a 2 decimales. Pista: round(math.pi, 2).
# Ejemplo:  pi_redondeado()  →  3.14
def pi_redondeado():
    """Devolvé math.pi con 2 decimales."""
    # TU CÓDIGO ACÁ
    pass


# Tirar un dado
# Devolvé un entero al azar entre 1 y 6. Pista: random.randint(1, 6).
# Ejemplo:  tirar_dado()  →  4   (un número de 1 a 6)
def tirar_dado():
    """Devolvé un número al azar de 1 a 6."""
    # TU CÓDIGO ACÁ
    pass


# Pokémon al azar
# Elegí un elemento al azar de la lista. Pista: random.choice.
# Ejemplo:  pokemon_al_azar(["Pikachu", "Onix"])  →  "Onix"   (al azar)
def pokemon_al_azar(lista):
    """Devolvé un elemento al azar de la lista."""
    # TU CÓDIGO ACÁ
    pass


# Mezclar la lista
# Devolvé una COPIA mezclada de la lista, sin modificar la original.
# Pista: copiá con list(lista) y usá random.shuffle sobre la copia.
def mezclar(lista):
    """Devolvé una copia mezclada de la lista."""
    # TU CÓDIGO ACÁ
    pass


# Fecha de hoy
# Devolvé la fecha de hoy en formato ISO. Pista: date.today().isoformat().
# Ejemplo:  fecha_hoy()  →  "2026-06-04"
def fecha_hoy():
    """Devolvé la fecha de hoy como 'AAAA-MM-DD'."""
    # TU CÓDIGO ACÁ
    pass


# Diccionario a JSON
# Convertí un diccionario a texto JSON. Pista: json.dumps.
# Ejemplo:  a_json({"nivel": 25})  →  '{"nivel": 25}'
def a_json(diccionario):
    """Devolvé el diccionario como texto JSON."""
    # TU CÓDIGO ACÁ
    pass


# JSON a diccionario
# Convertí un texto JSON a diccionario. Pista: json.loads.
# Ejemplo:  de_json('{"nivel": 25}')  →  {"nivel": 25}
def de_json(texto):
    """Devolvé el diccionario a partir del texto JSON."""
    # TU CÓDIGO ACÁ
    pass


# Guardar JSON en archivo
# Guardá un diccionario como JSON en el archivo. Pista: json.dump dentro de un with.
def guardar_json(ruta, datos):
    """Guardá 'datos' como JSON en el archivo 'ruta'."""
    # TU CÓDIGO ACÁ
    pass


# Cargar JSON de archivo
# Cargá y devolvé el diccionario del archivo JSON. Pista: json.load dentro de un with.
def cargar_json(ruta):
    """Cargá y devolvé el diccionario del archivo JSON."""
    # TU CÓDIGO ACÁ
    pass


# Nombre del archivo
# De una ruta completa, devolvé solo el nombre del archivo. Pista: os.path.basename.
# Ejemplo:  nombre_archivo("/home/ash/pokedex.txt")  →  "pokedex.txt"
def nombre_archivo(ruta):
    """Devolvé el nombre del archivo de la ruta."""
    # TU CÓDIGO ACÁ
    pass


# ¿Existe la ruta?
# Devolvé True si el archivo o carpeta existe. Pista: os.path.exists.
# Ejemplo:  existe("archivo_que_no_esta.txt")  →  False
def existe(ruta):
    """Devolvé True si la ruta existe."""
    # TU CÓDIGO ACÁ
    pass


# Tu módulo propio
# Usá tu módulo pokeutils: devolvé pokeutils.resumen(nombre, tipo, nivel).
# Ejemplo:  resumen_pokemon("Pikachu", "Electrico", 25)  →  el resumen que arma pokeutils
def resumen_pokemon(nombre, tipo, nivel):
    """Devolvé pokeutils.resumen(nombre, tipo, nivel)."""
    # TU CÓDIGO ACÁ
    pass

# Factorial
# Devolvé el factorial de n (n! = n × (n-1) × … × 1). Está en el módulo math.
# Ejemplo:  factorial_de(5)  →  120   ·   factorial_de(0)  →  1
def factorial_de(n):
    """Devolvé el factorial de n."""
    # TU CÓDIGO ACÁ
    pass


# Distancia entre dos puntos
# Devolvé la distancia en línea recta entre (x1, y1) y (x2, y2). El módulo math tiene
# una función que calcula la hipotenusa a partir de los dos catetos.
# Ejemplo:  distancia(0, 0, 3, 4)  →  5.0
def distancia(x1, y1, x2, y2):
    """Devolvé la distancia entre (x1, y1) y (x2, y2)."""
    # TU CÓDIGO ACÁ
    pass


# Equipo al azar (sin repetir)
# Elegí 'n' Pokémon al azar de la lista, SIN repetir ninguno. El módulo random tiene
# una función para tomar una muestra sin reemplazo.
# Ejemplo:  muestra_unica(["Pikachu", "Onix", "Eevee", "Gengar"], 2)  →  ["Eevee", "Onix"]  (al azar)
def muestra_unica(lista, n):
    """Devolvé n elementos al azar de la lista, sin repetir."""
    # TU CÓDIGO ACÁ
    pass


# Extensión del archivo
# De una ruta, devolvé solo la extensión, con el punto. El módulo os.path tiene una
# función que separa el nombre de la extensión.
# Ejemplo:  extension("pokedex.json")  →  ".json"   ·   extension("notas.txt")  →  ".txt"
def extension(ruta):
    """Devolvé la extensión del archivo (con el punto)."""
    # TU CÓDIGO ACÁ
    pass


# JSON ordenado por clave
# Convertí el diccionario a texto JSON con las claves ORDENADAS alfabéticamente.
# json.dumps tiene un parámetro para ordenar las claves.
# Ejemplo:  json_ordenado({"nivel": 25, "hp": 35})  →  '{"hp": 35, "nivel": 25}'
def json_ordenado(diccionario):
    """Devolvé el diccionario como JSON con las claves ordenadas."""
    # TU CÓDIGO ACÁ
    pass
