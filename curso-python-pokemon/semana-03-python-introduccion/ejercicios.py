"""
✏️ Semana 03 — Ejercicios: Python Introducción

Completá cada función donde dice '# TU CÓDIGO ACÁ'. Borrá el 'pass' (o el
'return None') cuando escribas tu solución.

Para probar TUS soluciones:
  1. Abrí test_ejercicios.py
  2. Cambiá la línea  modulo = _cargar("soluciones")  por  modulo = _cargar("ejercicios")
  3. Corré: pytest semana-03-python-introduccion/

Las soluciones completas están en soluciones.py (¡miralas recién después de intentar!).
"""


# ----------------------------------------------------------------------
# Ejercicio 1: Devolvé el texto "¡Hola, mundo Pokémon!"
# ----------------------------------------------------------------------
def saludo():
    """Devolvé exactamente el texto: ¡Hola, mundo Pokémon!"""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 2: Devolvé el nombre de tu Pokémon favorito (un str cualquiera).
# ----------------------------------------------------------------------
def mi_pokemon_favorito():
    """Devolvé un string con el nombre de un Pokémon (el que quieras)."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 3: Devolvé el doble del nivel recibido.
# ----------------------------------------------------------------------
def doble_nivel(nivel):
    """Recibí un número 'nivel' y devolvé su doble."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 4: Sumá dos números y devolvé el resultado.
# ----------------------------------------------------------------------
def suma(a, b):
    """Devolvé la suma de a y b."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 5: Restá b a a y devolvé el resultado.
# ----------------------------------------------------------------------
def resta(a, b):
    """Devolvé a menos b."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 6: Devolvé el promedio de tres stats (ataque, defensa, velocidad).
# ----------------------------------------------------------------------
def promedio_stats(ataque, defensa, velocidad):
    """Devolvé el promedio de los tres números (sumá y dividí por 3)."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 7: Convertí un texto a número entero y devolvelo.
# ----------------------------------------------------------------------
def a_entero(texto):
    """Recibí un str como '25' y devolvé el int 25."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 8: Convertí un número a texto y devolvelo.
# ----------------------------------------------------------------------
def a_texto(numero):
    """Recibí un número y devolvelo como str."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 9: Convertí un texto a número decimal (float) y devolvelo.
# ----------------------------------------------------------------------
def a_decimal(texto):
    """Recibí un str como '6.5' y devolvé el float 6.5."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 10: Devolvé el NOMBRE del tipo de dato del valor recibido.
# Pista: type(valor).__name__ te da 'int', 'str', etc.
# ----------------------------------------------------------------------
def nombre_del_tipo(valor):
    """Devolvé el nombre del tipo: 'int', 'str', 'float' o 'bool'."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 11: Armá una presentación con un f-string.
# Para nombre="Pikachu", nivel=25 → "Mi Pikachu es nivel 25"
# ----------------------------------------------------------------------
def presentacion(nombre, nivel):
    """Devolvé: Mi <nombre> es nivel <nivel>  (usá un f-string)."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 12: Armá una ficha de varias líneas con un f-string.
# Debe devolver exactamente (con saltos de línea \n):
#   Nombre: Pikachu
#   Tipo: Electrico
#   Nivel: 25
# ----------------------------------------------------------------------
def ficha(nombre, tipo, nivel):
    """Devolvé una ficha de 3 líneas con nombre, tipo y nivel."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 13: Calculá el HP total. Cada poción cura 20 puntos.
# total = hp_actual + cantidad_pociones * 20
# ----------------------------------------------------------------------
def hp_total(hp_actual, cantidad_pociones):
    """Devolvé el HP total sumando 20 por cada poción."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 14: Devolvé True si el nivel es par, False si es impar.
# Pista: un número es par si nivel % 2 == 0
# ----------------------------------------------------------------------
def nivel_es_par(nivel):
    """Devolvé True si el nivel es par, False si no."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicio 15: Fusioná dos nombres en uno solo (concatenación).
# Para "Char" y "izard" → "Charizard"
# ----------------------------------------------------------------------
def fusionar_nombres(parte1, parte2):
    """Devolvé los dos textos pegados (concatenados)."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# EJERCICIOS CON input() — estos interactúan con el usuario.
# (En los tests se simula lo que el usuario escribe.)
# ----------------------------------------------------------------------

# Ejercicio 16: Pedí el nombre del Pokémon con input() y devolvé un saludo.
# Si el usuario escribe "Pikachu" → devolvé "¡Hola, Pikachu!"
def pedir_nombre_y_saludar():
    """Usá input() para pedir un nombre y devolvé '¡Hola, <nombre>!'."""
    # TU CÓDIGO ACÁ
    pass


# Ejercicio 17: Pedí el nivel (texto) con input(), convertilo a int y devolvé
# el nivel + 1 (el Pokémon subió un nivel). Si escribe "25" → devolvé 26.
def pedir_nivel_y_subir():
    """Pedí un nivel con input(), convertilo a int y devolvé nivel + 1."""
    # TU CÓDIGO ACÁ
    pass


# Ejercicio 18: Pedí DOS números con input(), convertilos y devolvé su suma.
def pedir_dos_numeros_y_sumar():
    """Pedí dos números con input(), convertilos a int y devolvé la suma."""
    # TU CÓDIGO ACÁ
    pass


# Ejercicio 19: Pedí nombre y ciudad con input() y devolvé una presentación.
# Para "Ash" y "Pueblo Paleta" → "Soy Ash de Pueblo Paleta"
def registrar_entrenador():
    """Pedí nombre y ciudad con input() y devolvé 'Soy <nombre> de <ciudad>'."""
    # TU CÓDIGO ACÁ
    pass


# Ejercicio 20: Pedí un texto con input() y MOSTRALO con print() en mayúsculas
# dentro de un mensaje. Para "pikachu" debe imprimir: "Elegiste a PIKACHU"
# (Usá print, no return.)
def elegir_inicial():
    """Pedí un Pokémon con input() e imprimí 'Elegiste a <NOMBRE-EN-MAYUSCULAS>'."""
    # TU CÓDIGO ACÁ
    pass
