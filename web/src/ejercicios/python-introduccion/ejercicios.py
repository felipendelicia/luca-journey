"""✏️ Ejercicios — Python: Introducción

Completá cada función donde dice '# TU CÓDIGO ACÁ' y borrá el 'pass'.
Tocá ✅ Corregir para probar. ¡Arrancás tu viaje en Kanto! 🔴
"""


# Tu primer ¡Hola!
# Devolvé (con return) el texto EXACTO: ¡Hola, mundo Pokémon!
# Ojo con las comillas y los signos ¡ !
# Ejemplo:  saludo()  →  "¡Hola, mundo Pokémon!"
def saludo():
    """Devolvé el texto: ¡Hola, mundo Pokémon!"""
    # TU CÓDIGO ACÁ
    pass


# Tu Pokémon favorito
# Devolvé un texto con el nombre de cualquier Pokémon que te guste.
# Ejemplo:  mi_pokemon_favorito()  →  "Gengar"   (el que vos quieras)
def mi_pokemon_favorito():
    """Devolvé un string con el nombre de un Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Subida de nivel doble
# Recibís un 'nivel' y devolvés su doble (nivel × 2).
# Ejemplo:  doble_nivel(25)  →  50
def doble_nivel(nivel):
    """Devolvé el doble de 'nivel'."""
    # TU CÓDIGO ACÁ
    pass


# Sumar puntos
# Devolvé la suma de los dos números 'a' y 'b'.
# Ejemplo:  suma(3, 4)  →  7
def suma(a, b):
    """Devolvé a + b."""
    # TU CÓDIGO ACÁ
    pass


# Daño recibido
# Devolvé 'a' menos 'b' (por ejemplo, el HP que queda tras un golpe).
# Ejemplo:  resta(100, 30)  →  70
def resta(a, b):
    """Devolvé a - b."""
    # TU CÓDIGO ACÁ
    pass


# Promedio de stats
# Sumá ataque, defensa y velocidad, y dividí por 3.
# Ejemplo:  promedio_stats(90, 60, 30)  →  60.0
def promedio_stats(ataque, defensa, velocidad):
    """Devolvé el promedio de los tres números."""
    # TU CÓDIGO ACÁ
    pass


# Texto a número entero
# Convertí un texto como "25" en el número entero 25. Pista: int(...)
# Ejemplo:  a_entero("25")  →  25
def a_entero(texto):
    """Convertí 'texto' a int y devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Número a texto
# Convertí un número en su versión de texto. Pista: str(...)
# Ejemplo:  a_texto(25)  →  "25"
def a_texto(numero):
    """Convertí 'numero' a str y devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Texto a decimal
# Convertí un texto como "6.5" en el número decimal 6.5. Pista: float(...)
# Ejemplo:  a_decimal("6.5")  →  6.5
def a_decimal(texto):
    """Convertí 'texto' a float y devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# ¿De qué tipo es?
# Devolvé el NOMBRE del tipo de dato del valor: 'int', 'str', 'float' o 'bool'.
# Pista: type(valor).__name__
# Ejemplo:  nombre_del_tipo(25)  →  "int"
def nombre_del_tipo(valor):
    """Devolvé el nombre del tipo de 'valor'."""
    # TU CÓDIGO ACÁ
    pass


# Carta de presentación
# Con un f-string, devolvé: Mi <nombre> es nivel <nivel>
# Ejemplo:  presentacion("Pikachu", 25)  →  "Mi Pikachu es nivel 25"
def presentacion(nombre, nivel):
    """Devolvé 'Mi <nombre> es nivel <nivel>' usando un f-string."""
    # TU CÓDIGO ACÁ
    pass


# Ficha del Pokémon
# Devolvé una ficha de 3 líneas (separadas con \n):
#   Nombre: <nombre>
#   Tipo: <tipo>
#   Nivel: <nivel>
# Ejemplo:  ficha("Pikachu", "Electrico", 25)  →  "Nombre: Pikachu\nTipo: Electrico\nNivel: 25"
def ficha(nombre, tipo, nivel):
    """Devolvé una ficha de 3 líneas con nombre, tipo y nivel."""
    # TU CÓDIGO ACÁ
    pass


# Curar con pociones
# Cada poción cura 20 HP. Devolvé el HP total: hp_actual + pociones × 20.
# Ejemplo:  hp_total(50, 3)  →  110
def hp_total(hp_actual, cantidad_pociones):
    """Devolvé hp_actual + cantidad_pociones * 20."""
    # TU CÓDIGO ACÁ
    pass


# ¿Nivel par?
# Devolvé True si el nivel es par, y False si es impar. Pista: nivel % 2 == 0
# Ejemplo:  nivel_es_par(24)  →  True
def nivel_es_par(nivel):
    """Devolvé True si 'nivel' es par, False si no."""
    # TU CÓDIGO ACÁ
    pass


# Fusión de nombres
# Pegá (concatená) dos textos en uno solo.
# Ejemplo:  fusionar_nombres("Char", "izard")  →  "Charizard"
def fusionar_nombres(parte1, parte2):
    """Devolvé parte1 y parte2 pegados."""
    # TU CÓDIGO ACÁ
    pass


# Saludo interactivo
# Pedí un nombre con input() y devolvé '¡Hola, <nombre>!'.
# Ejemplo:  el usuario escribe "Pikachu"  →  "¡Hola, Pikachu!"
def pedir_nombre_y_saludar():
    """input() para pedir un nombre y devolver '¡Hola, <nombre>!'."""
    # TU CÓDIGO ACÁ
    pass


# Subir de nivel
# Pedí un nivel con input(), convertilo a int y devolvé nivel + 1.
# Ejemplo:  el usuario escribe "25"  →  26
def pedir_nivel_y_subir():
    """Pedí un nivel con input(), pasalo a int y devolvé nivel + 1."""
    # TU CÓDIGO ACÁ
    pass


# Sumar lo que te digan
# Pedí DOS números con input(), convertilos a int y devolvé su suma.
# Ejemplo:  el usuario escribe "10" y "15"  →  25
def pedir_dos_numeros_y_sumar():
    """Pedí dos números con input(), pasalos a int y devolvé la suma."""
    # TU CÓDIGO ACÁ
    pass


# Registro de Entrenador
# Pedí nombre y ciudad con input() y devolvé 'Soy <nombre> de <ciudad>'.
# Ejemplo:  "Ash" y "Pueblo Paleta"  →  "Soy Ash de Pueblo Paleta"
def registrar_entrenador():
    """Pedí nombre y ciudad con input() y devolvé 'Soy <nombre> de <ciudad>'."""
    # TU CÓDIGO ACÁ
    pass


# Elegir tu inicial
# Pedí un Pokémon con input() e IMPRIMÍ (con print) 'Elegiste a <NOMBRE EN MAYÚSCULAS>'.
# Pista: .upper() pone el texto en mayúsculas. Usá print, no return.
# Ejemplo:  el usuario escribe "pikachu"  →  imprime  Elegiste a PIKACHU
def elegir_inicial():
    """Pedí un Pokémon con input() e imprimí 'Elegiste a <NOMBRE>' en mayúsculas."""
    # TU CÓDIGO ACÁ
    pass
