"""🔑 Ejercicios — Variables de entorno y config

Las automatizaciones NO llevan contraseñas ni rutas escritas en el código: las leen
del ENTORNO o de un archivo de config (estilo .env). Acá parseás config y leés el
entorno. ✅ Corregí cuando termines.
"""
import os


# Parsear un archivo .env
# Un .env tiene líneas "CLAVE=valor". Devolvé un dict con esas claves y valores.
# Ignorá líneas vacías y comentarios (las que empiezan con #).
# Ejemplo:  parsear_env("API=abc\n# nota\nDEBUG=1")  →  {"API": "abc", "DEBUG": "1"}
def parsear_env(texto):
    """Devolvé un dict con las claves=valor del texto."""


# Obtener con defecto
# `config` es un dict. Devolvé el valor de `clave`, o `defecto` si no está.
# Ejemplo:  obtener({"A": "1"}, "A", "0")  →  "1"   ·   obtener({}, "A", "0")  →  "0"
def obtener(config, clave, defecto):
    """Devolvé config[clave] o defecto."""


# ¿Es un valor "verdadero"?
# En el entorno todo es texto. Devolvé True si `valor` (en minúsculas) es uno de:
# "1", "true", "si", "yes". Cualquier otra cosa → False.
# Ejemplo:  es_verdadero("TRUE")  →  True   ·   es_verdadero("no")  →  False
def es_verdadero(valor):
    """Devolvé True si valor representa verdadero."""


# Leer del entorno real
# Devolvé el valor de la variable de entorno `clave` (os.environ), o `defecto` si no
# existe. (os.environ.get hace justo esto.)
# Ejemplo:  leer_entorno("HOME", "/")  →  el valor de HOME (o "/" si no está)
def leer_entorno(clave, defecto):
    """Devolvé la variable de entorno clave, o defecto."""


# Claves
# Devolvé una lista con las claves del config.
def claves(config):
    """Devolvé las claves del dict."""
    # TU CÓDIGO ACÁ


# Valores
# Devolvé una lista con los valores del config.
def valores(config):
    """Devolvé los valores del dict."""
    # TU CÓDIGO ACÁ


# ¿Tiene la clave?
# Devolvé True si `clave` está en el config.
def tiene_clave(config, clave):
    """Devolvé True si la clave está."""
    # TU CÓDIGO ACÁ


# Cantidad
# Devolvé cuántas claves tiene el config.
def cantidad(config):
    """Devolvé cuántas claves hay."""
    # TU CÓDIGO ACÁ


# Serializar
# Convertí el config a texto estilo .env: una línea "CLAVE=valor" por cada par.
# Ejemplo:  serializar({"API": "abc", "DEBUG": "1"})  →  "API=abc\nDEBUG=1"
def serializar(config):
    """Devolvé el config como texto 'CLAVE=valor'."""
    # TU CÓDIGO ACÁ


# Fusionar
# Devolvé un dict nuevo con las claves de `base` y `extra`; si una clave está en ambos, gana
# la de `extra`.  Ejemplo:  fusionar({"A": "1", "B": "2"}, {"B": "9"})  →  {"A": "1", "B": "9"}
def fusionar(base, extra):
    """Devolvé base y extra fusionados (gana extra)."""
    # TU CÓDIGO ACÁ


# Solo con prefijo
# Devolvé un dict con las claves que empiezan con `prefijo`.
# Ejemplo:  solo_con_prefijo({"APP_A": "1", "DB_X": "2"}, "APP_")  →  {"APP_A": "1"}
def solo_con_prefijo(config, prefijo):
    """Devolvé las claves que empiezan con prefijo."""
    # TU CÓDIGO ACÁ


# A entero
# Devolvé config[clave] convertido a int; si no está o no se puede, devolvé `defecto`.
def a_entero(config, clave, defecto):
    """Devolvé int(config[clave]) o defecto."""
    # TU CÓDIGO ACÁ


# Requerir
# Devolvé config[clave]; si la clave no está, lanzá KeyError.
def requerir(config, clave):
    """Devolvé config[clave] o lanzá KeyError."""
    # TU CÓDIGO ACÁ


# Quitar comillas
# Si el valor empieza y termina con la misma comilla (" o '), devolvelo sin ellas; sino igual.
# Ejemplo:  quitar_comillas('"abc"')  →  "abc"   ·   quitar_comillas("abc")  →  "abc"
def quitar_comillas(valor):
    """Devolvé el valor sin las comillas de los extremos."""
    # TU CÓDIGO ACÁ


# ¿Es comentario?
# Devolvé True si la línea (sin espacios al inicio) empieza con "#".
def es_comentario(linea):
    """Devolvé True si la línea es un comentario."""
    # TU CÓDIGO ACÁ


# Contar líneas válidas
# Devolvé cuántas líneas del texto son pares CLAVE=valor (ni vacías ni comentarios, y con "=").
# Ejemplo:  contar_validas("A=1\n# nota\n\nB=2")  →  2
def contar_validas(texto):
    """Devolvé cuántas líneas válidas hay."""
    # TU CÓDIGO ACÁ


# Claves en mayúscula
# Devolvé un dict con las mismas claves pero en mayúscula.
def mayusculas_claves(config):
    """Devolvé el config con las claves en mayúscula."""
    # TU CÓDIGO ACÁ


# Default si vacío
# Devolvé config[clave]; si no está o su valor es "", devolvé `defecto`.
def con_default_si_vacio(config, clave, defecto):
    """Devolvé el valor, o defecto si falta o está vacío."""
    # TU CÓDIGO ACÁ


# Claves ordenadas
# Devolvé las claves ordenadas alfabéticamente.
def claves_ordenadas(config):
    """Devolvé las claves ordenadas."""
    # TU CÓDIGO ACÁ


# Invertir
# Devolvé un dict con claves y valores intercambiados.
def invertir(config):
    """Devolvé el config con clave y valor intercambiados."""
    # TU CÓDIGO ACÁ
