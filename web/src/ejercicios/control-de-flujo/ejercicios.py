"""✏️ Ejercicios — Control de Flujo

Decisiones (if/elif/else) y bucles (for/while). Completá cada función y tocá ✅ Corregir.
"""


# ¿Puede evolucionar?
# Devolvé True si el Pokémon puede evolucionar (nivel 25 o más), si no False.
# Ejemplo:  puede_evolucionar(30)  →  True
def puede_evolucionar(nivel):
    """Devolvé True si nivel >= 25."""
    # TU CÓDIGO ACÁ
    pass


# Estado según el HP
# Devolvé el estado:  hp > 70 → "sano" ,  hp > 30 → "herido" ,
#                     hp > 0  → "grave" ,  si no  → "debilitado".
# Ejemplo:  estado_hp(50)  →  "herido"
def estado_hp(hp):
    """Devolvé 'sano', 'herido', 'grave' o 'debilitado' según el hp."""
    # TU CÓDIGO ACÁ
    pass


# Ventaja de tipo
# Devolvé True si 'atacante' es súper efectivo contra 'defensor'.
# Reglas: fuego→planta, agua→fuego, planta→agua, electrico→agua.
# Ejemplo:  ventaja_tipo("agua", "fuego")  →  True
def ventaja_tipo(atacante, defensor):
    """Devolvé True si el atacante tiene ventaja sobre el defensor."""
    # TU CÓDIGO ACÁ
    pass


# El golpe más fuerte
# Devolvé el ataque mayor de los dos. Si empatan, devolvé 'ataque_a'.
# Ejemplo:  el_mas_fuerte(40, 75)  →  75
def el_mas_fuerte(ataque_a, ataque_b):
    """Devolvé el mayor; si empatan, ataque_a."""
    # TU CÓDIGO ACÁ
    pass


# Rango del Entrenador
# Clasificá por nivel:  nivel < 16 → "novato" ,  nivel < 40 → "intermedio" ,
#                       si no     → "experto".
# Ejemplo:  clasificar_nivel(20)  →  "intermedio"
def clasificar_nivel(nivel):
    """Devolvé 'novato', 'intermedio' o 'experto'."""
    # TU CÓDIGO ACÁ
    pass


# ¿Hay que curarlo?
# Devolvé True si el Pokémon necesita curarse (HP menor a 30).
# Ejemplo:  necesita_curarse(12)  →  True
def necesita_curarse(hp):
    """Devolvé True si hp < 30."""
    # TU CÓDIGO ACÁ
    pass


# Resultado del combate
# Comparando HP:  mi_hp > rival_hp → "ganaste" ,  mi_hp < rival_hp → "perdiste" ,
#                 iguales         → "empate".
# Ejemplo:  resultado_combate(80, 40)  →  "ganaste"
def resultado_combate(mi_hp, rival_hp):
    """Devolvé 'ganaste', 'perdiste' o 'empate'."""
    # TU CÓDIGO ACÁ
    pass


# Cuenta regresiva
# Para n=3 devolvé el texto "3,2,1,Ya!". Armalo con un bucle (for o while).
# Ejemplo:  cuenta_regresiva(3)  →  "3,2,1,Ya!"
def cuenta_regresiva(n):
    """Devolvé la cuenta regresiva como '3,2,1,Ya!'."""
    # TU CÓDIGO ACÁ
    pass


# Sumar del 1 al n
# Sumá todos los números del 1 al n (inclusive) usando un bucle.
# Ejemplo:  suma_1_a_n(5)  →  15   (1+2+3+4+5)
def suma_1_a_n(n):
    """Devolvé 1 + 2 + ... + n."""
    # TU CÓDIGO ACÁ
    pass


# Factorial
# Calculá n! = n × (n-1) × ... × 1.  Ojo: factorial(0) = 1.
# Ejemplo:  factorial(5)  →  120
def factorial(n):
    """Devolvé el factorial de n usando un bucle."""
    # TU CÓDIGO ACÁ
    pass


# Contar pares
# Contá cuántos números pares hay del 1 al n (inclusive).
# Ejemplo:  contar_pares(10)  →  5   (2,4,6,8,10)
def contar_pares(n):
    """Devolvé la cantidad de pares entre 1 y n."""
    # TU CÓDIGO ACÁ
    pass


# ¿Cuántos turnos?
# Cada turno le bajás 'dano' al 'hp_rival'. Contá los turnos hasta que el HP llegue a 0.
# Ejemplo:  cuantos_turnos(100, 30)  →  4   (30, 60, 90, 120)
def cuantos_turnos(hp_rival, dano):
    """Devolvé cuántos turnos de 'dano' hacen falta para que hp_rival llegue a 0."""
    # TU CÓDIGO ACÁ
    pass


# Potencia a mano
# Calculá base elevado a exp con un bucle, SIN usar el operador **.
# Ejemplo:  potencia(2, 5)  →  32
def potencia(base, exp):
    """Devolvé base ** exp pero calculado con un bucle."""
    # TU CÓDIGO ACÁ
    pass


# ¿Es primo?
# Devolvé True si n es primo (solo divisible por 1 y por sí mismo). 0 y 1 NO son primos.
# Ejemplo:  es_primo(7)  →  True
def es_primo(n):
    """Devolvé True si n es primo."""
    # TU CÓDIGO ACÁ
    pass


# Primer divisor
# Devolvé el divisor más chico de n que sea mayor que 1.
# Ejemplo:  primer_divisor(15)  →  3   ·   primer_divisor(7)  →  7
def primer_divisor(n):
    """Devolvé el divisor más chico de n mayor que 1."""
    # TU CÓDIGO ACÁ
    pass


# Contar vocales
# Contá cuántas vocales (a, e, i, o, u) tiene una palabra en minúsculas.
# Ejemplo:  contar_vocales("pikachu")  →  3
def contar_vocales(palabra):
    """Devolvé la cantidad de vocales en la palabra."""
    # TU CÓDIGO ACÁ
    pass


# El mayor de tres
# Devolvé el más grande de los tres números a, b y c.
# Ejemplo:  mayor_de_tres(40, 90, 12)  →  90
def mayor_de_tres(a, b, c):
    """Devolvé el mayor de a, b y c."""
    # TU CÓDIGO ACÁ
    pass


# Signo del número
# Devolvé "positivo", "negativo" o "cero" según el número.
# Ejemplo:  signo(-5)  →  "negativo"
def signo(numero):
    """Devolvé 'positivo', 'negativo' o 'cero'."""
    # TU CÓDIGO ACÁ
    pass


# ¿Está en el equipo?
# 'equipo' es una lista de nombres. Devolvé True si 'nombre' está. Usá un for con break.
# Ejemplo:  esta_en_equipo(["Pikachu", "Onix"], "Onix")  →  True
def esta_en_equipo(equipo, nombre):
    """Devolvé True si 'nombre' está en la lista 'equipo'."""
    # TU CÓDIGO ACÁ
    pass


# Pokémon debilitados
# 'equipo_hp' es una lista con el HP de cada Pokémon. Contá cuántos están a 0 o menos.
# Ejemplo:  contar_debilitados([100, 0, -5, 30])  →  2
def contar_debilitados(equipo_hp):
    """Devolvé cuántos valores de la lista son <= 0."""
    # TU CÓDIGO ACÁ
    pass
