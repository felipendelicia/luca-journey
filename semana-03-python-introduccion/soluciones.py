"""
✅ Semana 03 — Soluciones: Python Introducción

Cada función está comentada línea por línea explicando el razonamiento.
¡Mirá esto recién después de intentar los ejercicios vos!
"""


# Ejercicio 1
def saludo():
    """Devolvé exactamente el texto: ¡Hola, mundo Pokémon!"""
    # 'return' devuelve un valor desde la función. Acá devolvemos el texto.
    return "¡Hola, mundo Pokémon!"


# Ejercicio 2
def mi_pokemon_favorito():
    """Devolvé un string con el nombre de un Pokémon."""
    # Cualquier nombre de Pokémon como string sirve. Elegimos Pikachu.
    return "Pikachu"


# Ejercicio 3
def doble_nivel(nivel):
    """Devolvé el doble del nivel."""
    # Multiplicamos por 2 con el operador *.
    return nivel * 2


# Ejercicio 4
def suma(a, b):
    """Devolvé la suma de a y b."""
    # El operador + suma dos números.
    return a + b


# Ejercicio 5
def resta(a, b):
    """Devolvé a menos b."""
    # El operador - resta.
    return a - b


# Ejercicio 6
def promedio_stats(ataque, defensa, velocidad):
    """Devolvé el promedio de los tres números."""
    # Sumamos los tres y dividimos por 3. El / devuelve un float (decimal).
    return (ataque + defensa + velocidad) / 3


# Ejercicio 7
def a_entero(texto):
    """Convertí un texto a int."""
    # int() transforma un string que representa un número entero en un int.
    return int(texto)


# Ejercicio 8
def a_texto(numero):
    """Convertí un número a str."""
    # str() transforma cualquier valor en su versión de texto.
    return str(numero)


# Ejercicio 9
def a_decimal(texto):
    """Convertí un texto a float."""
    # float() transforma un string como "6.5" en el número decimal 6.5.
    return float(texto)


# Ejercicio 10
def nombre_del_tipo(valor):
    """Devolvé el nombre del tipo del valor."""
    # type(valor) da la clase; .__name__ da su nombre como string ('int', etc.).
    return type(valor).__name__


# Ejercicio 11
def presentacion(nombre, nivel):
    """Devolvé: Mi <nombre> es nivel <nivel>."""
    # El f-string mete las variables entre {} directamente en el texto.
    return f"Mi {nombre} es nivel {nivel}"


# Ejercicio 12
def ficha(nombre, tipo, nivel):
    """Devolvé una ficha de 3 líneas."""
    # \n es el "salto de línea": separa el texto en renglones.
    return f"Nombre: {nombre}\nTipo: {tipo}\nNivel: {nivel}"


# Ejercicio 13
def hp_total(hp_actual, cantidad_pociones):
    """Devolvé el HP total sumando 20 por cada poción."""
    # Primero multiplicamos las pociones por 20, después sumamos al HP actual.
    # Python respeta el orden matemático: * antes que +.
    return hp_actual + cantidad_pociones * 20


# Ejercicio 14
def nivel_es_par(nivel):
    """Devolvé True si el nivel es par."""
    # El operador % (módulo) da el resto de la división.
    # Si el resto de dividir por 2 es 0, el número es par.
    # La comparación == devuelve directamente True o False.
    return nivel % 2 == 0


# Ejercicio 15
def fusionar_nombres(parte1, parte2):
    """Devolvé los dos textos concatenados."""
    # El + entre strings los "pega" (concatena).
    return parte1 + parte2


# ----------------------------------------------------------------------
# EJERCICIOS CON input()
# ----------------------------------------------------------------------

# Ejercicio 16
def pedir_nombre_y_saludar():
    """Pedí un nombre con input() y devolvé un saludo."""
    # input() muestra el mensaje y espera que el usuario escriba algo.
    nombre = input("¿Nombre de tu Pokémon? ")
    # Armamos el saludo con un f-string y lo devolvemos.
    return f"¡Hola, {nombre}!"


# Ejercicio 17
def pedir_nivel_y_subir():
    """Pedí un nivel, convertilo a int y devolvé nivel + 1."""
    # input() devuelve texto, así que lo envolvemos en int() para tener un número.
    nivel = int(input("¿Nivel de tu Pokémon? "))
    # Le sumamos 1: subió de nivel.
    return nivel + 1


# Ejercicio 18
def pedir_dos_numeros_y_sumar():
    """Pedí dos números y devolvé la suma."""
    # Pedimos y convertimos cada número por separado.
    primero = int(input("Primer número: "))
    segundo = int(input("Segundo número: "))
    # Devolvemos la suma de ambos.
    return primero + segundo


# Ejercicio 19
def registrar_entrenador():
    """Pedí nombre y ciudad y devolvé una presentación."""
    nombre = input("¿Tu nombre? ")
    ciudad = input("¿Tu ciudad? ")
    # Combinamos ambos datos en una frase con un f-string.
    return f"Soy {nombre} de {ciudad}"


# Ejercicio 20
def elegir_inicial():
    """Pedí un Pokémon e imprimí el mensaje en mayúsculas."""
    eleccion = input("¿Qué Pokémon elegís? ")
    # .upper() convierte el texto a mayúsculas (lo vemos a fondo en la semana 7).
    # Acá usamos print() en vez de return porque el ejercicio pide MOSTRAR.
    print(f"Elegiste a {eleccion.upper()}")
