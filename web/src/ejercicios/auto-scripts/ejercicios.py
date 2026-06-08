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


# Primer argumento
# Devolvé el primer argumento de `argv`, o None si está vacío.
def primer_argumento(argv):
    """Devolvé argv[0], o None."""
    # TU CÓDIGO ACÁ


# Último argumento
# Devolvé el último argumento, o None si está vacío.
def ultimo_argumento(argv):
    """Devolvé el último argumento, o None."""
    # TU CÓDIGO ACÁ


# ¿Es una flag?
# Devolvé True si `arg` empieza con "-".
# Ejemplo:  es_flag("--verbose")  →  True   ·   es_flag("archivo.txt")  →  False
def es_flag(arg):
    """Devolvé True si arg es una flag."""
    # TU CÓDIGO ACÁ


# Solo las flags
# Devolvé los argumentos que son flags (empiezan con "-").
def solo_flags(argv):
    """Devolvé solo las flags."""
    # TU CÓDIGO ACÁ


# Sin flags
# Devolvé los argumentos que NO son flags.
def sin_flags(argv):
    """Devolvé los argumentos que no son flags."""
    # TU CÓDIGO ACÁ


# Cantidad de flags
# Devolvé cuántos argumentos son flags.
def cantidad_flags(argv):
    """Devolvé cuántas flags hay."""
    # TU CÓDIGO ACÁ


# Cantidad de posicionales
# Devolvé cuántos argumentos NO son flags (los posicionales).
def contar_posicionales(argv):
    """Devolvé cuántos posicionales hay."""
    # TU CÓDIGO ACÁ


# Posición de un argumento
# Devolvé el índice donde está `arg`, o -1 si no está.
def posicion_de(argv, arg):
    """Devolvé el índice de arg, o -1."""
    # TU CÓDIGO ACÁ


# ¿Están todas las flags?
# Devolvé True si TODAS las `flags` están en `argv`.
def tiene_todas_las_flags(argv, flags):
    """Devolvé True si están todas las flags."""
    # TU CÓDIGO ACÁ


# Quitar una flag
# Devolvé `argv` sin las apariciones de `flag`.
def quitar_flag(argv, flag):
    """Devolvé argv sin esa flag."""
    # TU CÓDIGO ACÁ


# Agregar una flag
# Agregá `flag` al final solo si no estaba. Devolvé argv.
def agregar_flag(argv, flag):
    """Agregá flag si no estaba."""
    # TU CÓDIGO ACÁ


# Normalizar una flag
# Devolvé la flag sin los guiones del inicio.
# Ejemplo:  normalizar_flag("--verbose")  →  "verbose"
def normalizar_flag(flag):
    """Devolvé la flag sin guiones iniciales."""
    # TU CÓDIGO ACÁ


# Valor con igual
# Buscá un argumento con la forma "clave=valor" y devolvé el valor, o None si no está.
# Ejemplo:  valor_con_igual(["--nivel=25"], "--nivel")  →  "25"
def valor_con_igual(argv, clave):
    """Devolvé el valor de 'clave=valor', o None."""
    # TU CÓDIGO ACÁ


# Juntar argumentos
# Devolvé todos los argumentos unidos por un espacio.
# Ejemplo:  juntar_argumentos(["python", "bot.py", "-v"])  →  "python bot.py -v"
def juntar_argumentos(argv):
    """Devolvé los argumentos unidos por espacios."""
    # TU CÓDIGO ACÁ


# Reemplazar una flag
# Devolvé `argv` con cada aparición de `viejo` cambiada por `nuevo`.
def reemplazar_flag(argv, viejo, nuevo):
    """Reemplazá viejo por nuevo en argv."""
    # TU CÓDIGO ACÁ


# ¿Hay flag repetida?
# Devolvé True si alguna flag aparece más de una vez.
def hay_flag_repetida(argv):
    """Devolvé True si hay una flag repetida."""
    # TU CÓDIGO ACÁ
