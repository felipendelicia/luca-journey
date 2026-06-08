"""
✅ Semana 10 — Soluciones: Módulos y pip

Comentadas línea por línea.
"""

import math
import random
import json
import os
from datetime import date

import pokeutils


# 1)
def raiz_cuadrada(n):
    """Raíz cuadrada."""
    # math.sqrt calcula la raíz cuadrada (devuelve float).
    return math.sqrt(n)


# 2)
def redondear_arriba(n):
    """Redondeo hacia arriba."""
    # math.ceil siempre redondea para arriba.
    return math.ceil(n)


# 3)
def redondear_abajo(n):
    """Redondeo hacia abajo."""
    # math.floor siempre redondea para abajo.
    return math.floor(n)


# 4)
def pi_redondeado():
    """Pi con 2 decimales."""
    # round(valor, decimales) recorta los decimales.
    return round(math.pi, 2)


# 5)
def tirar_dado():
    """Dado al azar 1-6."""
    # random.randint(a, b) incluye ambos extremos.
    return random.randint(1, 6)


# 6)
def pokemon_al_azar(lista):
    """Elemento al azar."""
    # random.choice elige un elemento al azar de la lista.
    return random.choice(lista)


# 7)
def mezclar(lista):
    """Copia mezclada."""
    # Copiamos para no tocar la original.
    copia = list(lista)
    # random.shuffle mezcla la lista en el lugar (modifica la copia).
    random.shuffle(copia)
    return copia


# 8)
def fecha_hoy():
    """Fecha de hoy en ISO."""
    # date.today() da la fecha; .isoformat() la convierte a 'AAAA-MM-DD'.
    return date.today().isoformat()


# 9)
def a_json(diccionario):
    """Diccionario a texto JSON."""
    return json.dumps(diccionario)


# 10)
def de_json(texto):
    """Texto JSON a diccionario."""
    return json.loads(texto)


# 11)
def guardar_json(ruta, datos):
    """Guardar JSON en archivo."""
    with open(ruta, "w", encoding="utf-8") as f:
        # json.dump escribe el diccionario directamente en el archivo.
        json.dump(datos, f)


# 12)
def cargar_json(ruta):
    """Cargar JSON desde archivo."""
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


# 13)
def nombre_archivo(ruta):
    """Nombre del archivo."""
    # os.path.basename devuelve la última parte de la ruta.
    return os.path.basename(ruta)


# 14)
def existe(ruta):
    """¿Existe la ruta?"""
    return os.path.exists(ruta)


# 15)
def resumen_pokemon(nombre, tipo, nivel):
    """Usa el módulo propio pokeutils."""
    # Reusamos una función de nuestro módulo.
    return pokeutils.resumen(nombre, tipo, nivel)


# 16) Factorial — math.factorial calcula n!
def factorial_de(n):
    return math.factorial(n)


# 17) Distancia — math.hypot(cateto_x, cateto_y) da la hipotenusa
def distancia(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


# 18) Muestra única — random.sample toma n elementos sin repetir
def muestra_unica(lista, n):
    return random.sample(lista, n)


# 19) Extensión — os.path.splitext separa (nombre, extensión)
def extension(ruta):
    return os.path.splitext(ruta)[1]


# 20) JSON ordenado — sort_keys=True ordena las claves alfabéticamente
def json_ordenado(diccionario):
    return json.dumps(diccionario, sort_keys=True)
