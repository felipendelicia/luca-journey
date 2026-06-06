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
