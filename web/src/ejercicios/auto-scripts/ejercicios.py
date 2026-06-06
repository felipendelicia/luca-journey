"""⚙️ Ejercicios — Scripts y argumentos

Un script de automatización recibe ARGUMENTOS desde la terminal
(python bot.py --nivel 30 --shiny). Acá los leés: primero a mano (sys.argv es una
lista de textos) y después con argparse. ✅ Corregí cuando termines.
"""
import argparse


# Contar argumentos reales
# sys.argv es la lista de la terminal: el PRIMERO (argv[0]) es el nombre del script
# y el resto son los argumentos. Devolvé cuántos argumentos REALES hay (todos menos
# el nombre del script).
# Ejemplo:  contar_argumentos(["bot.py", "--nivel", "30"])  →  2
#           contar_argumentos(["bot.py"])  →  0
def contar_argumentos(argv):
    """Devolvé la cantidad de argumentos sin contar argv[0]."""


# ¿Está la bandera?
# Una bandera (flag) es un argumento como "--shiny" que está o no está. Devolvé True
# si `flag` aparece en la lista `argv`, o False si no.
# Ejemplo:  flag_presente(["bot.py", "--shiny"], "--shiny")  →  True
#           flag_presente(["bot.py"], "--shiny")  →  False
def flag_presente(argv, flag):
    """Devolvé True si flag está en argv."""


# Valor de una opción
# Algunas opciones traen un valor JUSTO DESPUÉS: en ["--nivel", "30"] el valor de
# "--nivel" es "30". Devolvé el texto que viene después de `flag` en `argv`. Si la
# opción no está, o no hay nada después de ella, devolvé `defecto`.
# Ejemplo:  valor_de(["bot.py","--nivel","30"], "--nivel", "1")  →  "30"
#           valor_de(["bot.py"], "--nivel", "1")  →  "1"
def valor_de(argv, flag, defecto=None):
    """Devolvé el valor que sigue a flag en argv, o defecto."""


# Parsear con argparse
# Armá un ArgumentParser con estas tres opciones y devolvé los valores como dict:
#   --nivel  : entero, por defecto 1
#   --nombre : texto, por defecto "Pikachu"
#   --shiny  : bandera (action="store_true")
# Parseá la lista `argv` y devolvé un diccionario con las claves "nivel", "nombre",
# "shiny". Recordá: parser.parse_args(argv) devuelve un Namespace y vars(...) lo
# convierte en dict.
# Ejemplo:  parsear(["--nivel","30","--shiny"])  →  {"nivel":30,"nombre":"Pikachu","shiny":True}
def parsear(argv):
    """Definí el parser, parseá argv y devolvé vars(args)."""
