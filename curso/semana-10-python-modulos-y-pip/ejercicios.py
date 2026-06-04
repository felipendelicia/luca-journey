"""
✏️ Semana 10 — Ejercicios: Módulos y pip

15 ejercicios usando módulos de la librería estándar (math, random, json,
datetime, os) y tu módulo propio pokeutils.

Completá donde dice '# TU CÓDIGO ACÁ'. Respuestas en soluciones.py.
Para probar tu trabajo: en test_ejercicios.py cambiá _cargar("soluciones")
por _cargar("ejercicios").
"""

import math
import random
import json
import os
from datetime import date

import pokeutils  # nuestro módulo propio (está al lado de este archivo)


# 1) Devolvé la raíz cuadrada de n (usá math).
def raiz_cuadrada(n):
    """Devolvé la raíz cuadrada de n."""
    # TU CÓDIGO ACÁ
    pass


# 2) Redondeá n para ARRIBA (usá math.ceil). 4.1 -> 5
def redondear_arriba(n):
    """Devolvé n redondeado hacia arriba."""
    # TU CÓDIGO ACÁ
    pass


# 3) Redondeá n para ABAJO (usá math.floor). 4.9 -> 4
def redondear_abajo(n):
    """Devolvé n redondeado hacia abajo."""
    # TU CÓDIGO ACÁ
    pass


# 4) Devolvé pi redondeado a 2 decimales (usá math.pi y round). -> 3.14
def pi_redondeado():
    """Devolvé math.pi con 2 decimales."""
    # TU CÓDIGO ACÁ
    pass


# 5) Tirá un dado: devolvé un entero al azar entre 1 y 6 (usá random.randint).
def tirar_dado():
    """Devolvé un número al azar de 1 a 6."""
    # TU CÓDIGO ACÁ
    pass


# 6) Elegí un Pokémon al azar de la lista (usá random.choice).
def pokemon_al_azar(lista):
    """Devolvé un elemento al azar de la lista."""
    # TU CÓDIGO ACÁ
    pass


# 7) Devolvé una COPIA mezclada de la lista (no modifiques la original).
#    Pista: copiá con list(lista) y usá random.shuffle sobre la copia.
def mezclar(lista):
    """Devolvé una copia mezclada de la lista."""
    # TU CÓDIGO ACÁ
    pass


# 8) Devolvé la fecha de hoy como texto ISO (usá date.today().isoformat()).
def fecha_hoy():
    """Devolvé la fecha de hoy como 'AAAA-MM-DD'."""
    # TU CÓDIGO ACÁ
    pass


# 9) Convertí un diccionario a texto JSON (usá json.dumps).
def a_json(diccionario):
    """Devolvé el diccionario como texto JSON."""
    # TU CÓDIGO ACÁ
    pass


# 10) Convertí un texto JSON a diccionario (usá json.loads).
def de_json(texto):
    """Devolvé el diccionario a partir del texto JSON."""
    # TU CÓDIGO ACÁ
    pass


# 11) Guardá un diccionario en un archivo JSON (usá json.dump dentro de un with).
def guardar_json(ruta, datos):
    """Guardá 'datos' como JSON en el archivo 'ruta'."""
    # TU CÓDIGO ACÁ
    pass


# 12) Cargá un diccionario desde un archivo JSON (usá json.load dentro de un with).
def cargar_json(ruta):
    """Cargá y devolvé el diccionario del archivo JSON 'ruta'."""
    # TU CÓDIGO ACÁ
    pass


# 13) Devolvé solo el nombre del archivo de una ruta (usá os.path.basename).
#     "/home/ash/pokedex.txt" -> "pokedex.txt"
def nombre_archivo(ruta):
    """Devolvé el nombre del archivo de la ruta."""
    # TU CÓDIGO ACÁ
    pass


# 14) Devolvé True si el archivo/carpeta de 'ruta' existe (usá os.path.exists).
def existe(ruta):
    """Devolvé True si la ruta existe."""
    # TU CÓDIGO ACÁ
    pass


# 15) Usá tu MÓDULO PROPIO: devolvé el resumen de un Pokémon usando
#     pokeutils.resumen(nombre, tipo, nivel).
def resumen_pokemon(nombre, tipo, nivel):
    """Devolvé pokeutils.resumen(nombre, tipo, nivel)."""
    # TU CÓDIGO ACÁ
    pass
